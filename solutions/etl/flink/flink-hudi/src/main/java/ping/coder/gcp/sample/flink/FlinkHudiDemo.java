package ping.coder.gcp.sample.flink;

import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.functions.source.SourceFunction;
import org.apache.flink.table.api.bridge.java.StreamTableEnvironment;

import org.apache.flink.table.data.GenericRowData;
import org.apache.flink.table.data.RowData;
import org.apache.hudi.common.model.HoodieTableType;
import org.apache.hudi.configuration.FlinkOptions;
import org.apache.hudi.util.HoodiePipeline;

import java.util.HashMap;
import java.util.Map;

import static jodd.util.ThreadUtil.sleep;

public class FlinkHudiDemo {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        // start Table Environment
        StreamTableEnvironment tableEnv =
                StreamTableEnvironment.create(env);
        env.setParallelism(1);
        env.enableCheckpointing(1000);
//        tableEnv.executeSql(
//                "CREATE CATALOG peace_catalog WITH (\n" +
//                        "  'type'='iceberg',\n" +
//                        "  'catalog-type'='hive',\n" +
//                        "  'uri'='thrift://cluster-flink-m:9083',\n" +
//                        "  'clients'='5',\n" +
//                        "  'property-version'='1',\n" +
//                        "  'warehouse'='gs://peace-us-byd-hive/warehouse/'\n" +
//                        ");"
//        );
//        String catalogName = "peace_catalog";
//        String database = "iceberg";
//
//        tableEnv.useCatalog(catalogName);
//
//        tableEnv.executeSql("create database IF NOT EXISTS iceberg;");
//        tableEnv.useDatabase(database);

        // Create a table in hive catalog
//        tableEnv.executeSql("TScreate table IF NOT EXIS first_table (name varchar(32) PRIMARY KEY NOT ENFORCED, age int) PARTITIONED BY (age) WITH(" +
//                        "'connector' = 'hudi'," +
//                        "'path' = 'gs://peace-us-byd-hive/warehouse/hudi.db/first_table'," +
//                        "'hive_sync.enable' = 'true'," +
//                        "'hive_sync.mode' = 'hms'," +
//                        "'hive_sync.metastore.uris' = 'thrift://10.128.15.228:9083'" +
//                ");");

//        tableEnv.executeSql("INSERT INTO first_table VALUES('123', 12);").print();
//
//        tableEnv.executeSql("SELECT * from first_table;").print();
        DataStream<RowData> ds = env.addSource(new SourceFunction<RowData>(){
            boolean isRunning = true;
            int index = 1;

            @Override
            public void run(SourceContext<RowData> sourceContext) throws Exception {

                while(isRunning && index < 100){
                    System.out.println("Write a row: name"+index);
                    GenericRowData row = new GenericRowData(2);
                    row.setField(0, "name:+"+index);
                    row.setField(1, 10 + index);
                    sourceContext.collect(row);
                    index++;
                    sleep(10 * 1000);
                }
            }

            @Override
            public void cancel() {
                isRunning = false;
            }
        });

        Map<String, String> options = new HashMap<>();
        options.put(FlinkOptions.PATH.key(), "gs://peace-us-byd-hive/warehouse/hudi.db/first_table");
        options.put(FlinkOptions.HIVE_SYNC_ENABLED.key(), "true");
        options.put(FlinkOptions.HIVE_SYNC_MODE.key(), "hms");
        options.put(FlinkOptions.HIVE_SYNC_METASTORE_URIS.key(), "thrift://10.128.15.228:9083");

        HoodiePipeline.Builder builder = HoodiePipeline.builder("first_table")
                .column("name VARCHAR(32)")
                .column("age INT")
                .pk("name")
                .partition("age")
                .options(options);

        builder.sink(ds, true); // The second parameter indicating whether the input data stream is bounded
        env.execute("Api_Sink");

        // Read from the table and print the results
//        tableEnv.from("iceberg_table").execute().print();
        // 4. run stream
//        env.execute("Hive Demo on Flink");
    }
}