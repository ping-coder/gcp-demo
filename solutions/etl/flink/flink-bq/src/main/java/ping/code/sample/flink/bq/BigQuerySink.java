package ping.code.sample.flink.bq;

import java.io.IOException;

import org.apache.flink.api.connector.sink2.Sink;
import org.apache.flink.api.connector.sink2.SinkWriter;
import org.apache.flink.table.data.RowData;

public class BigQuerySink implements Sink<RowData>{

    @Override
    public SinkWriter<RowData> createWriter(InitContext context) throws IOException {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'createWriter'");
    }

}
