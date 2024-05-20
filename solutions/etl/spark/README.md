## 1. Spark to Iceberg and Hudi.

### on Dataproc 2.0 with Hudi

edit file '/usr/lib/spark/conf/spark-defaults.conf'
```conf
spark.sql.extensions=org.apache.spark.sql.hudi.HoodieSparkSessionExtension,org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions
spark.sql.catalog.spark_catalog=org.apache.iceberg.spark.SparkSessionCatalog
```

spark-sql --packages org.apache.iceberg:iceberg-spark-runtime-3.3_2.12:1.4.3
or
upload ./lib/iceberg-spark-runtime-3.3_2.12-1.4.3.jar to /usr/lib/spark/jars/
or edit file '/usr/lib/spark/conf/spark-defaults.conf'
```conf
spark.driver.extraClassPath=/usr/lib/hudi/lib/hudi-spark3.3-bundle_2.12-0.12.3.1.jar:/usr/lib/iceberg/lib/iceberg-spark-runtime-3.3_2.12-1.4.3.jar
spark.executor.extraClassPath=/usr/lib/hudi/lib/hudi-spark3.3-bundle_2.12-0.12.3.1.jar:/usr/lib/iceberg/lib/iceberg-spark-runtime-3.3_2.12-1.4.3.jar
```