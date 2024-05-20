package ping.coder.gcp.sample.flink;

import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.table.api.bridge.java.StreamTableEnvironment;

public class FlinkIcebergDemo {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        // start Table Environment
        StreamTableEnvironment tableEnv =
                StreamTableEnvironment.create(env);
        env.setParallelism(1);
        env.enableCheckpointing(1000);
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
        String database = "iceberg";

        tableEnv.useCatalog(catalogName);

        tableEnv.executeSql("create database IF NOT EXISTS iceberg;");
        tableEnv.useDatabase(database);

        // Create a table in hive catalog
        tableEnv.executeSql("create table IF NOT EXISTS iceberg_table (name varchar(32), age int) PARTITIONED BY (age) ;");

        tableEnv.executeSql("INSERT INTO iceberg_table VALUES('123', 12);").print();

        tableEnv.executeSql("SELECT * from iceberg_table;").print();

        // Read from the table and print the results
        tableEnv.from("iceberg_table").execute().print();
        // 4. run stream
        env.execute("Hive Demo on Flink");
    }
}