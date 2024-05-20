package ping.coder.gcp.sample.flink;

import org.apache.flink.streaming.api.functions.source.SourceFunction;
import org.apache.flink.table.data.GenericRowData;
import org.apache.flink.table.data.RowData;
import org.apache.flink.table.data.StringData;
import org.apache.flink.table.data.TimestampData;

import static jodd.util.ThreadUtil.sleep;

public class SimpleRowDataSourceFunction {
    public static class RowDataSourceFunction implements SourceFunction<RowData> {
        boolean isRunning = true;
        int index = 1;

        @Override
        public void run(SourceContext<RowData> sourceContext) throws Exception {

            while (isRunning && index < 3) {
                System.out.println("Write a row: name" + index);
                GenericRowData row = new GenericRowData(4);
                row.setField(0, StringData.fromString("region-" + index));
                row.setField(1, StringData.fromString("name:n-" + index));
                row.setField(2, 10 + index);
                row.setField(3, TimestampData.fromEpochMillis(System.currentTimeMillis()));
                sourceContext.collect(row);
                index++;
                sleep(10 * 1000);
            }

            isRunning = false;
        }

        @Override
        public void cancel() {
            isRunning = false;
        }
    }
}
