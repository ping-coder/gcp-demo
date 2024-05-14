

```
gsutil cp gs://peace-us-byd-hive/flink/iceberg-hive-runtime-1.4.3.jar /usr/lib/hive/lib/
gsutil cp gs://peace-us-byd-hive/flink/iceberg-hive-runtime-1.4.3.jar /usr/lib/flink/lib/
gsutil cp gs://peace-us-byd-hive/flink/flink-connector-hive_2.12-1.15.0.jar /usr/lib/flink/lib/
gsutil cp gs://peace-us-byd-hive/flink/flink-sql-connector-hive-3.1.2_2.12-1.15.0.jar /usr/lib/flink/lib/
gsutil cp gs://peace-us-byd-hive/flink/iceberg-flink-runtime-1.15-1.4.3.jar /usr/lib/flink/lib/
gsutil cp gs://peace-us-byd-hive/flink/flink-iceberg-1.0-SNAPSHOT.jar ./

/usr/lib/flink/bin/flink run -c ping.coder.gcp.sample.flink.FlinkIcebergDemo flink-iceberg-1.0-SNAPSHOT.jar

/usr/lib/flink/bin/flink run-application -t yarn-application  -c ping.coder.gcp.sample.flink.FlinkIcebergDemo flink-iceberg-1.0-SNAPSHOT.jar

/usr/lib/flink/bin/sql-client.sh
```


```
SET iceberg.catalog.another_hive.type=hive;
SET iceberg.catalog.another_hive.uri=thrift://localhost:9083;
SET iceberg.catalog.another_hive.clients=5;
SET iceberg.catalog.another_hive.warehouse=gs://peace-us-byd-hive/warehouse/;
```


```
mvn install:install-file -Dfile='lib/gcs-connector-hadoop3-2.2.22-shaded.jar' -DgroupId='com.google.cloud.bigdataoss' -DartifactId=gcs-connector -Dversion='hadoop3-2.2.22-shaded' -Dpackaging=jar -DgeneratePom=true
```