#!/usr/bin/env python

"""BigQuery I/O PySpark example."""

from pyspark.sql import SparkSession

spark = SparkSession \
  .builder \
  .appName('spark-bigquery-demo') \
  .getOrCreate()

bigquery_table = "peace-demo.demo.trips_result"
# Use the Cloud Storage bucket for temporary BigQuery export data used
# by the connector.
bucket = "gs://peace-demo/staging"
spark.conf.set('temporaryGcsBucket', bucket)
spark.conf.set("viewsEnabled","true")
spark.conf.set("materializationDataset","demo")

# # Load data from BigQuery.
# trips = spark.read.format('bigquery') \
#   .option('table', 'bigquery-public-data:new_york_taxi_trips.tlc_yellow_trips_*') \
#   .load()
# trips.createOrReplaceTempView('trips')

sql = """
    SELECT 
        vendor_id,
        AVG(total_amount) AS avg_revenue,
        AVG(trip_distance) as avg_distance,
        count(*) as number
    FROM `bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_*` WHERE 
        trip_distance > 0 AND
        fare_amount > 0
    GROUP BY vendor_id
    ORDER BY avg_revenue DESC
"""
trips_result = spark.read.format("bigquery").load(sql)
trips_result.show()
trips_result.printSchema()

# Save the data to BigQuery
trips_result.write.format('bigquery') \
  .option('table', bigquery_table) \
  .save()