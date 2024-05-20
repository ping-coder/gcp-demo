package ping.coder.gcp.sample.flink;

import org.apache.flink.configuration.Configuration;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.table.api.EnvironmentSettings;
import org.apache.flink.table.api.bridge.java.StreamTableEnvironment;
import org.apache.flink.table.data.RowData;
import org.apache.hudi.common.table.HoodieTableConfig;
import org.apache.hudi.config.HoodieWriteConfig;
import org.apache.hudi.configuration.FlinkOptions;
import org.apache.hudi.util.HoodiePipeline;

import java.util.HashMap;
import java.util.Map;

public class FlinkSqlHudiDemo {
    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        conf.setString(HoodieTableConfig.DROP_PARTITION_COLUMNS.key(), "true");
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment(conf);
        // start Table Environment
        StreamTableEnvironment tableEnv =
                StreamTableEnvironment.create(env, EnvironmentSettings.newInstance().withConfiguration(conf).build());

        env.setParallelism(1);
        env.enableCheckpointing(20000);
        tableEnv.executeSql(
                "CREATE CATALOG peace_catalog WITH (\n" +
                        "  'type'='iceberg',\n" +
                        "  'catalog-type'='hive',\n" +
                        "  'uri'='thrift://cluster-flink-m:9083',\n" +
                        "  'clients'='5',\n" +
                        "  'property-version'='1',\n" +
                        "  'warehouse'='gs://peace-us-byd-hive/warehouse/'\n" +
                        ");"
        );
        String catalogName = "peace_catalog";
        tableEnv.useCatalog(catalogName);

        String database = "hudi.db";
        tableEnv.executeSql("create database IF NOT EXISTS hudi.db;");
        tableEnv.useDatabase(database);

//         Create a table in hive catalog
        String createTableSql = "create table IF NOT EXISTS drop_down_table (name varchar(32) PRIMARY KEY NOT ENFORCED, age INT, ts TIMESTAMP(3)) PARTITIONED BY (age) WITH(" +
                "'connector' = 'hudi'," +
                "'path' = 'gs://peace-us-byd-hive/warehouse/hudi.db/sql_hudi_table/'," +
                "'hive_sync.enable' = 'true'," +
                "'hive_sync.mode' = 'hms'," +
                "'hoodie.datasource.write.hive_style_partitioning' = 'true'," +
                "'hoodie.datasource.write.drop.partition.columns' = 'true'," +
                "'hoodie.datasource.hive_sync.partition_fields' = 'age'," +
                "'write.hive_style_partitioning' = 'true'," +
                "'write.drop.partition.columns' = 'true'," +
                "'hive_sync.metastore.uris' = 'thrift://10.128.15.228:9083'" +
                ");";

        tableEnv.executeSql(createTableSql).print();

        String insertSQL = "INSERT INTO sql_hudi_table VALUES('region123', 'name123', 12, TIMESTAMP '2024-5-18 00:08:00');";
        tableEnv.executeSql(insertSQL).print();

        Map<String, String> options = new HashMap<>();
        options.put(FlinkOptions.PATH.key(), "gs://peace-us-byd-hive/warehouse/hudi.db/sql_hudi_table");
        options.put(FlinkOptions.HIVE_SYNC_ENABLED.key(), "true");
        options.put(FlinkOptions.HIVE_SYNC_MODE.key(), "hms");
        options.put(FlinkOptions.HIVE_SYNC_METASTORE_URIS.key(), "thrift://10.128.0.10:9083");
        options.put(FlinkOptions.TABLE_TYPE.key(), FlinkOptions.TABLE_TYPE_COPY_ON_WRITE);
        options.put(FlinkOptions.CLUSTERING_ASYNC_ENABLED.key(), "true");
        options.put(HoodieTableConfig.PRECOMBINE_FIELD.key(), "nots");
        options.put(FlinkOptions.PRECOMBINE_FIELD.key(), "nots");
        options.put(HoodieWriteConfig.PRECOMBINE_FIELD_NAME.key(), "nots");
        options.put(FlinkOptions.HIVE_STYLE_PARTITIONING.key(),"true");
        options.put(HoodieTableConfig.DROP_PARTITION_COLUMNS.key(),"true");
        options.put("hoodie.datasource.write.drop.partition.columns", "true");
        options.put("write.drop.partition.columns", "true");

        DataStream<RowData> ds = env.addSource(new SimpleRowDataSourceFunction.RowDataSourceFunction());
//

        HoodiePipeline.Builder builder = HoodiePipeline.builder("sql_hudi_table")
                .column("region VARCHAR(32)")
                .column("name VARCHAR(32)")
                .column("age INT")
                .column("nots TIMESTAMP(3)")
                .pk("name")
                .partition("region", "age")
                .options(options);

        builder.sink(ds, true); // The second parameter indicating whether the input data stream is bounded

        // 4. run stream
        env.execute("Hive Demo on Flink");
    }

}