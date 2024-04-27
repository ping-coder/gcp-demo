package ping.code.sample;

import com.google.api.core.ApiFuture;
import com.google.api.core.ApiFutures;
import com.google.api.gax.core.FixedCredentialsProvider;
import com.google.auth.oauth2.GoogleCredentials;
import com.google.auth.oauth2.ServiceAccountCredentials;
import com.google.cloud.pubsub.v1.Publisher;
import com.google.common.collect.ImmutableMap;
import com.google.protobuf.ByteString;
import com.google.pubsub.v1.PubsubMessage;
import com.google.pubsub.v1.TopicName;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.streaming.api.functions.sink.RichSinkFunction;

import java.io.InputStream;
import java.util.concurrent.TimeUnit;

public class GcpSink extends RichSinkFunction<Tuple2<String, String>> {

    String projectId;
    String topicId;
    Publisher publisher = null;
    GoogleCredentials credentials = null;


    public GcpSink(String projectId, String topicId) {
        this.projectId = projectId;
        this.topicId = topicId;
    }

    @Override
    public void open(Configuration parameters) throws Exception {
        System.out.println("Open GcpSink ....");
        this.credentials = ServiceAccountCredentials.fromStream(getAutheficateFile());
    }

    @Override
    public void close() throws Exception {
        System.out.println("Close GcpSink ....");
        if (publisher != null) {
            // When finished with the publisher, shutdown to free up resources.
            publisher.shutdown();
            publisher.awaitTermination(1, TimeUnit.MINUTES);
        }
    }

    @Override
    public void invoke(Tuple2<String, String> value, Context context) throws Exception {
        System.out.println("Invoke GcpSink ....");
        TopicName topicName = TopicName.of(projectId, topicId);

        // Create a publisher instance with default settings bound to the topic
        publisher = Publisher.newBuilder(topicName).setCredentialsProvider(FixedCredentialsProvider.create(credentials)).build();

        ByteString data = ByteString.copyFromUtf8(value.f1);
        PubsubMessage pubsubMessage =
                PubsubMessage.newBuilder()
                        .setData(data)
                        .putAllAttributes(ImmutableMap.of("ATTR_TABLE_NAME", value.f0))
                        .build();

        // Once published, returns a server-assigned message id (unique within the topic)
        ApiFuture<String> messageIdFuture = publisher.publish(pubsubMessage);
        String messageId = messageIdFuture.get();
        System.out.println("Published a message with custom attributes: " + messageId);
    }

    public static InputStream getAutheficateFile() {
        String configFile = "/peace_demo_meitu_flink_key.json";
        InputStream credentialsFile = StreamingJob.class.getResourceAsStream(configFile);
        return credentialsFile;
    }
}
