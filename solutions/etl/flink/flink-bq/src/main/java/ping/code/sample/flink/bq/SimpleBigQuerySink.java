package ping.code.sample.flink.bq;

import java.net.Inet4Address;
import java.util.concurrent.Executors;
import java.util.concurrent.Flow.Publisher;

import org.apache.flink.streaming.api.functions.sink.RichSinkFunction;
import org.json.JSONArray;
import org.json.JSONObject;

import com.google.api.core.ApiFuture;
import com.google.api.core.ApiFutures;
import com.google.api.gax.core.FixedExecutorProvider;
import com.google.cloud.bigquery.storage.v1.AppendRowsRequest;
import com.google.cloud.bigquery.storage.v1.AppendRowsResponse;
import com.google.cloud.bigquery.storage.v1.BigQueryWriteClient;
import com.google.cloud.bigquery.storage.v1.BigQueryWriteSettings;
import com.google.cloud.bigquery.storage.v1.JsonStreamWriter;
import com.google.cloud.bigquery.storage.v1.TableName;
import com.google.common.util.concurrent.MoreExecutors;

/**
 * This document describes how to use the BigQuery Storage Write API to stream data into BigQuery. <br/>
 * 1. Use the default stream for at-least-once semantics. <br/>
 * 2. Use committed type for exactly-once semantics. <br/>
 * 3. Use multiplexing. <br/>
 * @see https://cloud.google.com/bigquery/docs/write-api-streaming?hl=zh-cn
 */
public class SimpleBigQuerySink extends RichSinkFunction<String> {

    String projectId = "peace-demo";
    String datasetName = "sample";
    String tableName = "t_simple_flink_to_bq_sink";

    @Override
    public void invoke(String value, Context context) throws Exception {
        System.out.println("Invoke SimpleBigQuerySink ....");

        String ipAddress = Inet4Address.getLocalHost().getHostAddress();
        TableName parentTable = TableName.of(projectId, datasetName, tableName);
        // Initialize client without settings, internally within stream writer a new client will be
        // created with full settings.
        BigQueryWriteClient client = BigQueryWriteClient.create();
        // Use the JSON stream writer to send records in JSON format. Specify the table name to write to the default stream.
        // For more information about JsonStreamWriter, see:
        // https://googleapis.dev/java/google-cloud-bigquerystorage/latest/com/google/cloud/bigquery/storage/v1/JsonStreamWriter.html
        JsonStreamWriter writer = JsonStreamWriter.newBuilder(parentTable.toString(), client)
                                        .setExecutorProvider(FixedExecutorProvider.create(Executors.newScheduledThreadPool(100)))
                                        .setChannelProvider(
                                            BigQueryWriteSettings.defaultGrpcTransportProviderBuilder()
                                                .setKeepAliveTime(org.threeten.bp.Duration.ofMinutes(1))
                                                .setKeepAliveTimeout(org.threeten.bp.Duration.ofMinutes(1))
                                                .setKeepAliveWithoutCalls(true)
                                                .build())
                                        .setEnableConnectionPool(true)
                                        // If value is missing in json and there is a default value configured on bigquery
                                        // column, apply the default value to the missing value field.
                                        .setDefaultMissingValueInterpretation(AppendRowsRequest.MissingValueInterpretation.DEFAULT_VALUE)
                                        .build();
        // 
        JSONArray jsonArr = new JSONArray();
        JSONObject record = new JSONObject();
        record.put("id", value);
        record.put("ip_address", ipAddress);
        jsonArr.put(record);
        // Append asynchronously for increased throughput.
        writer.append(jsonArr);

        client.close();
        // Close the connection to the server.
        writer.close();

        System.out.println("Appended a row to bigquery table with attributes: id=" + value + ", ip address=" + ipAddress);
    }
}
