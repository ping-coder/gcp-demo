# install
## general
https://github.com/GoogleCloudDataproc/initialization-actions/blob/master/opsagent/README.md

no syslog
```bash
REGION=<region>
CLUSTER_NAME=<cluster_name>
gcloud dataproc clusters create ${CLUSTER_NAME} \
    --image-version=2.2 \
    --region=${REGION} \
    --initialization-actions=gs://goog-dataproc-initialization-actions-${REGION}/opsagent/opsagent_nosyslog.sh
```

## apache hbase
https://cloud.google.com/stackdriver/docs/solutions/agents/ops-agent/third-party/hbase?hl=zh-cn



# reference
ops hbase metrics:
https://cloud.google.com/monitoring/api/metrics_opsagent#opsagent-hbase
