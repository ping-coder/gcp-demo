# install jmx exporter
https://github.com/prometheus/jmx_exporter

download jmx_prometheus_httpserver-0.20.0.jar 

copy hbase_exporter_rule.yaml to hbase master and regionalserver

modify port in hbase_exporter_rule.yaml
```yml
hostPort: localhost:[port]
```

run standalone HTTP server
```bash
java -jar jmx_prometheus_httpserver-0.20.0.jar 12345 hbase_exporter_rule.yaml
```

run web preview on cloud shell
```bash
export PROJECT=peace-demo;export HOSTNAME=cluster-hbase-m;export ZONE=us-central1-c
PORT1=12345
PORT2=12345
gcloud compute ssh ${HOSTNAME} \
    --project=${PROJECT} --zone=${ZONE}  -- \
    -4 -N -L ${PORT1}:${HOSTNAME}:${PORT2}
```