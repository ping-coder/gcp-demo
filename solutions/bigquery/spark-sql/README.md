gsutil cp ./solutions/bigquery/spark-sql/sample_sql_newyork.py gs://peace-demo/upload/

gs://peace-demo/upload/sample_sql_newyork.py

gcloud dataproc batches submit --project peace-demo --region us-central1 pyspark --batch batch-142c gs://peace-demo/upload/sample_sql_newyork.py --version 2.2 --subnet default


gsutil cp ./solutions/bigquery/spark-sql/sample_sql_newyork.sql gs://peace-demo/upload/

gs://peace-demo/upload/sample_sql_newyork.sql

gcloud dataproc batches submit --project peace-demo --region us-central1 spark-sql --batch batch-495a gs://peace-demo/upload/sample_sql_newyork.sql --version 2.2 --subnet default