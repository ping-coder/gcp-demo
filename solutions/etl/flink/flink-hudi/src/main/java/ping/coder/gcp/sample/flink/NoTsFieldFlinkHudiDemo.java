package ping.coder.gcp.sample.flink;

import org.apache.flink.configuration.Configuration;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.table.data.RowData;
import org.apache.hudi.common.table.HoodieTableConfig;
import org.apache.hudi.config.HoodieWriteConfig;
import org.apache.hudi.configuration.FlinkOptions;
import org.apache.hudi.util.HoodiePipeline;

import java.util.HashMap;
import java.util.Map;

public class NoTsFieldFlinkHudiDemo {
    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        conf.setString(HoodieTableConfig.DROP_PARTITION_COLUMNS.key(), "true");
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment(conf);

        Map<String, String> options = new HashMap<>();
        options.put(FlinkOptions.PATH.key(), "gs://peace-us-byd-hive/warehouse/hudi.db/no_ts_table");
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

        HoodiePipeline.Builder builder = HoodiePipeline.builder("no_ts_table")
                .column("region VARCHAR(32)")
                .column("name VARCHAR(32)")
                .column("age INT")
                .column("nots TIMESTAMP(3)")
                .pk("name")
                .partition("region", "age")
                .options(options);

        builder.sink(ds, true); // The second parameter indicating whether the input data stream is bounded

        env.execute("Hive Demo on Flink");
    }

}