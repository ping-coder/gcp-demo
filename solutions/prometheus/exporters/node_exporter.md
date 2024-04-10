# install
参考：https://cloud.google.com/stackdriver/docs/managed-prometheus/exporters/node_exporter

Connect to the managed service for prometheus cluster
```
gcloud container clusters get-credentials [cluster-name] --zone us-central1-c --project peace-demo
```

```
kubectl apply -f node_exporter.yaml
```

```
kubectl apply -f node_exporter_rule.yaml
```