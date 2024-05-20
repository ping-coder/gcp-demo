### 1. BigQuerySyncTool
仅0.14.0以上版本支持Manifest File的同步模式，该工具功能可参考文档：https://hudi.apache.org/docs/next/gcp_bigquery 

上述文档未写明的一个特性是：0.14.1的版本相比0.14.0版本，增加配置项"--big-lake-connection-id {BigLake connection id}"，使用此配置项可以直接生成BigLake表，不使用则是外部表。

使用如下：（必须加载./sync/lib/目录的所以依赖包）
1. 权限和Biglake连接
参看此处文档即可：https://cloud.google.com/bigquery/docs/query-open-table-format-using-manifest-files?hl=zh-cn#required_roles
检查项：
- [可选] 如果使用BigQuery的Spark存储过程，则需要创建Spark连接，以及为该连接对应的service account设置roles/storage.objectAdmin IAM 角色
- [必须] Biglake的Connection必须有roles/storage.objectAdmin IAM 角色
- [必须] 运行环境（如在VM中）的service account必须要有roles/storage.objectAdmin, roles/bigquery.connectionUser, roles/bigquery.dataViewer, roles/bigquery.user的 IAM 角色
2. 环境变量
```bash
export project_id={bq_project_id}
export dataset_id={bq_dataset_id}
export dataset_location={bq_dataset_location}
export table_name={bq_table_name}
export hudi_source_uri={hudi_table_gcs_path}
export hudi_source_uri_prefix={hudi_table_gcs_path_prefix}
export hudi_base_path={hudi_table_gcs_path_prefix}
export biglake_conn_id={biglake_connection_id}
export partitioned_by={partition_keys}
```
3. 在sync目录下，直接运行Java
```bash
sudo java -cp ./hudi-gcp-bundle-0.14.1.jar:./lib/*: \
org.apache.hudi.gcp.bigquery.BigQuerySyncTool \
--project-id $project_id \
--dataset-name $dataset_id \
--dataset-location $dataset_location \
--source-uri $hudi_source_uri \
--source-uri-prefix $hudi_source_uri_prefix \
--base-path $hudi_base_path \
--table $table_name \
--partitioned-by $partitioned_by \
--base-file-format PARQUET \
--big-lake-connection-id $biglake_conn_id \
--decode-partition \
--sync-incremental \
--use-bq-manifest-file
```

注：dataproc 2.1的hudi为0.12.3，其hudi-spark-bundle包有冲突，无法直接用spark任务运行。

3. 检查
- 查看"gs://../warehouse/table/.hoodie/absolute-path-manifest"目录下的文件"latest-snapshot.csv"
- 查看BigQuery新建的表


### 2. Dataproc 2.1
1. 权限和Biglake连接
参看此处文档即可：https://cloud.google.com/bigquery/docs/query-open-table-format-using-manifest-files?hl=zh-cn#required_roles
检查项：
- [可选] 如果使用BigQuery的Spark存储过程，则需要创建Spark连接，以及为该连接对应的service account设置roles/storage.objectAdmin IAM 角色
- [必须] Biglake的Connection必须有roles/storage.objectAdmin IAM 角色
- [必须] 运行环境（如在VM中）的service account必须要有roles/storage.objectAdmin, roles/bigquery.connectionUser, roles/bigquery.dataViewer, roles/bigquery.user的 IAM 角色
- [必须] 必须安装Hudi和Trino

2. 复制lib
将lib下的jar包复制到/usr/lib/spark/jars/，并复制sync 工具包（只能使用dataproc内0.12.3.1的版本）
```bash
sudo cp /usr/lib/hudi/tools/bq-sync-tool/hudi-gcp-bundle-0.12.3.1.jar /usr/lib/spark/jars/
```

3. 运行命令：
```bash
sudo spark-submit \
--packages com.google.cloud:google-cloud-bigquery:2.10.4 \
--jars /usr/lib/hudi/tools/bq-sync-tool/hudi-gcp-bundle-0.12.3.1.jar \
--class org.apache.hudi.utilities.deltastreamer.HoodieDeltaStreamer \
  /usr/lib/spark/jars/hudi-utilities-bundle_2.12-0.12.3.jar \
--target-base-path gs://.../warehouse/target_table_path \
--target-table table_name \
--table-type COPY_ON_WRITE \
--source-class org.apache.hudi.utilities.sources.ParquetDFSSource \
--base-file-format PARQUET \
--enable-sync \
--sync-tool-classes org.apache.hudi.gcp.bigquery.BigQuerySyncTool \
--hoodie-conf hoodie.deltastreamer.source.dfs.root=gs://.../warehouse/source_table_path \
--hoodie-conf hoodie.gcp.bigquery.sync.project_id=project-id \
--hoodie-conf hoodie.gcp.bigquery.sync.dataset_name=dataset \
--hoodie-conf hoodie.gcp.bigquery.sync.dataset_location=dataset-location \
--hoodie-conf hoodie.gcp.bigquery.sync.table_name=table_name \
--hoodie-conf hoodie.gcp.bigquery.sync.partition_fields=key1,key2 \
--hoodie-conf hoodie.gcp.bigquery.sync.base_path=gs://.../warehouse/source_table_path \
--hoodie-conf hoodie.gcp.bigquery.sync.source_uri=gs://.../warehouse/source_table_path/partition_key_path=* \
--hoodie-conf hoodie.gcp.bigquery.sync.source_uri_prefix=gs://.../warehouse/source_table_path/ \
--hoodie-conf hoodie.gcp.bigquery.sync.use_file_listing_from_metadata=false \
--hoodie-conf hoodie.gcp.bigquery.sync.assume_date_partitioning=false \
--hoodie-conf hoodie.gcp.bigquery.sync.use_bq_manifest_file=false \
--hoodie-conf hoodie.datasource.hive_sync.use_jdbc=false \
--hoodie-conf hoodie.datasource.hive_sync.mode=hms \
--hoodie-conf hoodie.datasource.hive_sync.metastore.uris=thrift://ip_address:9083 \
--hoodie-conf hoodie.datasource.hive_sync.skip_ro_suffix=true \
--hoodie-conf hoodie.datasource.hive_sync.ignore_exceptions=false \
--hoodie-conf hoodie.datasource.hive_sync.table=table_name \
--hoodie-conf hoodie.datasource.write.recordkey.field=pk \
--hoodie-conf hoodie.datasource.write.partitionpath.field=key1,key2 \
--hoodie-conf hoodie.datasource.write.precombine.field=ts \
--hoodie-conf hoodie.table.precombine.field=ts \
--hoodie-conf hoodie.datasource.write.keygenerator.type=COMPLEX \
--hoodie-conf hoodie.datasource.write.hive_style_partitioning=true \
--hoodie-conf hoodie.datasource.write.drop.partition.columns=true \
--hoodie-conf hoodie.partition.metafile.use.base.format=true \
--hoodie-conf hoodie.metadata.enable=true 
```