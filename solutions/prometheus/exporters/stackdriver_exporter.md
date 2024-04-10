# install
参考：https://github.com/prometheus-community/stackdriver_exporter?tab=readme-ov-file

Connect to the managed service for prometheus cluster
```bash
gcloud container clusters get-credentials [cluster-name] --zone us-central1-c --project peace-demo
```

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
# Helm 3
helm install [RELEASE NAME] prometheus-community/prometheus-stackdriver-exporter --set stackdriver.projectId=[google-project-name]
```

## Example
If we want to get all CPU (compute.googleapis.com/instance/cpu) and Disk (compute.googleapis.com/instance/disk) metrics for all Google Compute Engine instances, we can run the exporter with the following options:
```bash
stackdriver_exporter \
  --google.project-id=my-test-project \
  --monitoring.metrics-type-prefixes "compute.googleapis.com/instance/cpu,compute.googleapis.com/instance/disk"
helm upgrade [RELEASE NAME] prometheus-community/prometheus-stackdriver-exporter --set stackdriver.projectId=[google-project-name] --set metrics.typePrefixes="compute.googleapis.com/instance/cpu,compute.googleapis.com/instance/disk"
```

helm upgrade v1 prometheus-community/prometheus-stackdriver-exporter --set stackdriver.projectId=peace-demo --set metrics.typePrefixes="compute.googleapis.com/instance/cpu"