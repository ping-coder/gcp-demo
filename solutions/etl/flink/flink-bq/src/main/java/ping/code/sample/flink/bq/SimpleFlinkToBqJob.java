package ping.code.sample.flink.bq;

import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.common.typeinfo.Types;
import org.apache.flink.streaming.api.datastream.DataStreamSource;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.api.connector.source.util.ratelimit.RateLimiterStrategy;
import org.apache.flink.connector.datagen.source.DataGeneratorSource;
import org.apache.flink.connector.datagen.source.GeneratorFunction;

/**
 * table:
 * id - string
 * ip_address - String
 */
public class SimpleFlinkToBqJob 
{
    public static void main( String[] args ) throws Exception
    {
        final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.setParallelism(2);
        
        GeneratorFunction<Long, String> generatorFunction = index -> "Number: " + index;

        DataGeneratorSource<String> generatorSource =
                new DataGeneratorSource<>(
                        generatorFunction,
                        Long.MAX_VALUE,
                        RateLimiterStrategy.perSecond(4),
                        Types.STRING);

        DataStreamSource<String> streamSource =
                env.fromSource(generatorSource, WatermarkStrategy.noWatermarks(), "Data Generator");
        streamSource.print();
        streamSource.addSink(new SimpleBigQuerySink());

        env.execute("Flink to BigQuery Sample");
    }
}
