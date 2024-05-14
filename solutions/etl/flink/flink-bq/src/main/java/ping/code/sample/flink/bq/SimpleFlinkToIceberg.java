package ping.code.sample.flink.bq;

import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.connector.source.util.ratelimit.RateLimiterStrategy;
import org.apache.flink.configuration.RestOptions;
import org.apache.flink.connector.datagen.source.DataGeneratorSource;
import org.apache.flink.connector.datagen.source.GeneratorFunction;
import org.apache.flink.streaming.api.datastream.DataStreamSource;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.hadoop.conf.Configuration;
import org.apache.iceberg.catalog.TableIdentifier;
import org.apache.iceberg.hadoop.HadoopCatalog;
import org.apache.iceberg.Schema;
import org.apache.iceberg.types.Types;
import org.apache.iceberg.Table;

public class SimpleFlinkToIceberg {
    
    public static void main( String[] args ) throws Exception
    {
        org.apache.flink.configuration.Configuration flinkConf = new org.apache.flink.configuration.Configuration();
        flinkConf.setString(RestOptions.BIND_PORT,"8081");
        final StreamExecutionEnvironment env = StreamExecutionEnvironment.createLocalEnvironmentWithWebUI(flinkConf);
        env.setParallelism(2);

        Configuration conf = new Configuration();

        String warehousePath = "gs://peace-demo/sample/flink-to-bq/catalog";
        HadoopCatalog catalog = new HadoopCatalog(conf, warehousePath);
        TableIdentifier name = TableIdentifier.of("logging", "logs");
        Schema schema = new Schema(
                                Types.NestedField.required(1, "level", Types.StringType.get()),
                                Types.NestedField.required(2, "event_time", Types.TimestampType.withZone()),
                                Types.NestedField.required(3, "message", Types.StringType.get()),
                                Types.NestedField.optional(4, "call_stack", Types.ListType.ofRequired(5, Types.StringType.get()))
                            );
        Table table = catalog.createTable(name, schema);
        catalog.close();

        GeneratorFunction<Long, String> generatorFunction = index -> "Number: " + index;
        DataGeneratorSource<String> generatorSource =
                new DataGeneratorSource<>(
                        generatorFunction,
                        Long.MAX_VALUE,
                        RateLimiterStrategy.perSecond(4),
                        org.apache.flink.api.common.typeinfo.Types.STRING);

        DataStreamSource<String> streamSource =
                env.fromSource(generatorSource, WatermarkStrategy.noWatermarks(), "Data Generator");
        streamSource.print(catalog.name());

        env.execute("Flink to Iceberg Sample");
    }
}
