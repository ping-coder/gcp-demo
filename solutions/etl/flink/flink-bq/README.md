# run flink

1. Run yarn-session in dataproc master:
```bash
sudo /usr/lib/flink/bin/yarn-session.sh \
 -s 1 \
 -jm 2048m \
 -tm 2048m \
 -nm flink-dataproc \
 --detached
```

```bash
flink run -c ping.code.sample.flink.bq.SimpleFlinkToBqJob original-flink-bq-1.0-SNAPSHOT.jar

flink run -c ping.code.sample.flink.bq.SimpleFlinkToBqJob flink-bq-1.0-SNAPSHOT.jar

flink run -c ping.code.sample.flink.bq.SimpleFlinkToBqJob gs://peace-demo/sample/flink-to-bq/flink-bq-1.0-SNAPSHOT.jar
```


```bash
flink run \
    -m yarn-cluster \
    -p 2 \
    -ys 1 \
    -yjm 1024m \
    -ytm 2048m \
    -c ping.code.sample.flink.bq.SimpleFlinkToBqJob \
    flink-bq-1.0-SNAPSHOT.jar
```

```bash
flink run \
    -m yarn-cluster \
    -p 2 \
    -ys 1 \
    -yjm 1024m \
    -ytm 2048m \
    -c ping.code.sample.flink.bq.SimpleFlinkToIceberg \
    flink-bq-1.0-SNAPSHOT.jar
```


```bash
gcloud builds submit --tag us-central1-docker.pkg.dev/peace-demo/gcf-artifacts/flink2bq

./bin/flink run-application --target kubernetes-application -Dkubernetes.cluster-id=autopilot-flink -Dkubernetes.container.image.ref=us-central1-docker.pkg.dev/peace-demo/gcf-artifacts/flink2bq:v1 -c ping.code.sample.flink.bq.SimpleFlinkToIceberg  local:///opt/flink/flink-bq-1.0-SNAPSHOT.jar

./bin/flink list --target kubernetes-application -Dkubernetes.cluster-id=autopilot-flink

./bin/kubernetes-session.sh -Dkubernetes.cluster-id=autopilot-flink -Dexecution.attached=true

./bin/flink run --target kubernetes-session -Dkubernetes.cluster-id=autopilot-flink ./examples/streaming/TopSpeedWindowing.jar
```

```bash
cp D:\projects\github\ping.coder\gcp-demo\solutions\etl\flink\flink-bq\target\flink-bq-1.0-SNAPSHOT.jar D:\projects\flink-1.17.2\lib\
./bin/standalone-job.sh start --job-classname ping.code.sample.flink.bq.SimpleFlinkToIceberg
./bin/taskmanager.sh start

./bin/start-cluster.sh
./bin/flink run -c ping.code.sample.flink.bq.SimpleFlinkToIceberg ./lib/flink-bq-1.0-SNAPSHOT.jar
```