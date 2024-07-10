## TPC-DS
https://github.com/maropu/spark-tpcds-datagen

## AWS

### Generate TPC-DS data
1. (Option) create a emr cluster to generate TPC-DS data.
1. SSH Connect to master node.
1. (Option) install git on master node.
1. Clone git repo:
    ``` bash
    cd ~
    sudo yum install -y git
    git clone https://github.com/maropu/spark-tpcds-datagen.git
    ```
1. Generate TPC-DS data to s3 bucket.
    ```bash
    cd spark-tpcds-datagen
    export SPARK_HOME=/usr/lib/spark/
    nohup ./bin/dsdgen --overwrite --scale-factor 50 --output-location s3://<your bucket>/spark-tpcds-data-50GB/ >output.log 2>&1 &
    nohup ./bin/dsdgen --overwrite --scale-factor 200 --output-location s3://<your bucket>/spark-tpcds-data-200GB/ >output.log 2>&1 &
    ```
1. (Option) Generate Partitioned TPC-DS data to s3 bucket.
    ```bash
    nohup ./bin/dsdgen --overwrite --scale-factor 200 --partition-tables --num-partitions 1 --output-location s3://<your bucket>/spark-tpcds-data-200GB-partitioned/ >output.log 2>&1 &
    nohup ./bin/dsdgen --overwrite --scale-factor 1000 --partition-tables --num-partitions 1 --output-location s3://<your bucket>/spark-tpcds-data-1TB-partitioned/ >output.log 2>&1 &
    ```
1. (Option) Stop emr cluster.
### TEST machine type "r6a-2xlarge"
1. Create emr cluster.
    ```bash
    aws emr create-cluster \
    --name "tpcds-test" \
    --log-uri "s3://<your bucket>/elasticmapreduce" \
    --release-label "emr-7.1.0" \
    --service-role "arn:aws:iam::<account>:role/<role>" \
    --unhealthy-node-replacement \
    --ec2-attributes '{"InstanceProfile":"<AmazonEMR InstanceProfile id>","EmrManagedMasterSecurityGroup":"<SecurityGroup ID>","EmrManagedSlaveSecurityGroup":"<SecurityGroup ID>","SubnetId":"<Subnet Id>"}' \
    --applications Name=Hadoop Name=Hive Name=JupyterEnterpriseGateway Name=Livy Name=Spark \
    --instance-groups '[{"InstanceCount":1,"InstanceGroupType":"MASTER","Name":"主节点","InstanceType":"m6a.2xlarge","EbsConfiguration":{"EbsBlockDeviceConfigs":[{"VolumeSpecification":{"VolumeType":"gp2","SizeInGB":32},"VolumesPerInstance":2}],"EbsOptimized":true}},{"InstanceCount":6,"InstanceGroupType":"CORE","Name":"核心节点","InstanceType":"r6a.2xlarge","EbsConfiguration":{"EbsBlockDeviceConfigs":[{"VolumeSpecification":{"VolumeType":"gp2","SizeInGB":128},"VolumesPerInstance":4}],"EbsOptimized":true}}]' \
    --scale-down-behavior "TERMINATE_AT_TASK_COMPLETION" \
    --ebs-root-volume-size "50" \
    --region "us-east-1"
    ```
1. SSH Connect to master node.
1. submit the spark job .
    ```bash
    aws emr add-steps --region us-east-1 --cluster-id "<EMR cluster id>"                 \
    --steps Type=Spark,Name="TPCDS Benchmark Job",                                      \
    Args=[--deploy-mode,cluster,                                                        \
    --class,org.apache.spark.sql.execution.benchmark.TPCDSQueryBenchmark,               \
    --conf,spark.driver.cores=4,                                                        \
    --conf,spark.driver.memory=16g,                                                     \
    --conf,spark.executor.cores=4,                                                      \
    --conf,spark.executor.memory=8g,                                                    \
    --conf,spark.network.timeout=2000,                                                  \
    --conf,spark.executor.heartbeatInterval=300s,                                       \
    --conf,spark.dynamicAllocation.enabled=true,                                        \
    --conf,spark.sql.shuffle.partitions=92,                                             \
    --conf,spark.sql.files.maxPartitionBytes=1073741824,                                \
    /usr/lib/spark/sql/core/target/spark-sql_<scala.version>-<spark.version>-tests.jar, \
    --data-location,s3://<your bucket>/spark-tpcds-data-50GB/,                          \
    ],ActionOnFailure=CONTINUE                                                          \
    > s3://<your bucket>/spark-tpcds-data-50GB-result/                                  
    ```

## GCP
### Generate TPC-DS data
1. (Option) create a dataproc cluster to generate TPC-DS data.
1. SSH Connect to master node.
1. (Option) install git on master node.
1. Clone git repo:
    ``` bash
    cd ~
    sudo yum install -y git
    git clone https://github.com/maropu/spark-tpcds-datagen.git
    ```
1. Generate TPC-DS data to gcs bucket.
    ```bash
    cd spark-tpcds-datagen
    export SPARK_HOME=/usr/lib/spark/
    nohup ./bin/dsdgen --overwrite --scale-factor 50 --output-location gs://<your bucket>/spark-tpcds-data-50GB/ >output.log 2>&1 &
    nohup ./bin/dsdgen --overwrite --scale-factor 200 --output-location gs://<your bucket>/spark-tpcds-data-200GB/ >output.log 2>&1 &
    ```
1. (Option) Generate Partitioned TPC-DS data to gcs bucket.
    ```bash
    nohup ./bin/dsdgen --overwrite --scale-factor 200 --partition-tables --num-partitions 1 --output-location gs://<your bucket>/spark-tpcds-data-200GB-partitioned/ >output.log 2>&1 &
    nohup ./bin/dsdgen --overwrite --scale-factor 1000 --partition-tables --num-partitions 1 --output-location gs://<your bucket>/spark-tpcds-data-1TB-partitioned/ >output.log 2>&1 &
    ```
1. (Option) Stop emr cluster.
### TEST machine type "n2d-highmem-8"
1. Create dataproc cluster.
    ```bash
    gcloud dataproc clusters create cluster-tpcds \
    --enable-component-gateway --region us-central1 --no-address --project <project id> \
    --master-machine-type n2d-standard-8 --master-boot-disk-type pd-balanced --master-boot-disk-size 100 --num-master-local-ssds 1 --master-local-ssd-interface NVME \
    --num-workers 6 --worker-machine-type n2d-highmem-8 --worker-boot-disk-type pd-balanced --worker-boot-disk-size 100 --num-worker-local-ssds 2 --worker-local-ssd-interface NVME \
    --image-version 2.2-debian12  --max-idle 600s \
    --properties core:fs.gs.metadata.cache.enable=true,spark:spark.dataproc.enhanced.optimizer.enabled=true,spark:spark.dataproc.enhanced.execution.enabled=true,dataproc:dataproc.cluster.caching.enabled=true \
    --scopes https://www.googleapis.com/auth/cloud-platform
    ```
1. submit the spark job .
    ```bash
    aws emr add-steps --region us-east-1 --cluster-id "<EMR cluster id>"                 \
    --steps Type=Spark,Name="TPCDS Benchmark Job",                                      \
    Args=[--deploy-mode,cluster,                                                        \
    --class,org.apache.spark.sql.execution.benchmark.TPCDSQueryBenchmark,               \
    --conf,spark.driver.cores=4,                                                        \
    --conf,spark.driver.memory=16g,                                                     \
    --conf,spark.executor.cores=4,                                                      \
    --conf,spark.executor.memory=8g,                                                    \
    --conf,spark.network.timeout=2000,                                                  \
    --conf,spark.executor.heartbeatInterval=300s,                                       \
    --conf,spark.dynamicAllocation.enabled=true,                                        \
    --conf,spark.sql.shuffle.partitions=92,                                             \
    --conf,spark.sql.files.maxPartitionBytes=1073741824,                                \
    /usr/lib/spark/sql/core/target/spark-sql_<scala.version>-<spark.version>-tests.jar, \
    --data-location,s3://<your bucket>/spark-tpcds-data-50GB/,                          \
    ],ActionOnFailure=CONTINUE                                                          \
    > s3://<your bucket>/spark-tpcds-data-50GB-result/                                  
    ```
    gcloud dataproc clusters create cluster-tpcds \
    --enable-component-gateway --region us-central1 --no-address --project peace-demo \
    --master-machine-type n2d-standard-8 --master-boot-disk-type pd-balanced --master-boot-disk-size 100 --num-master-local-ssds 1 --master-local-ssd-interface NVME \
    --num-workers 6 --worker-machine-type n2d-highmem-8 --worker-boot-disk-type pd-balanced --worker-boot-disk-size 100 --num-worker-local-ssds 2 --worker-local-ssd-interface NVME \
    --image-version 2.2-debian12  --max-idle 600s \
    --properties core:fs.gs.metadata.cache.enable=true,spark:spark.dataproc.enhanced.optimizer.enabled=true,spark:spark.dataproc.enhanced.execution.enabled=true,dataproc:dataproc.cluster.caching.enabled=true \
    --scopes https://www.googleapis.com/auth/cloud-platform

    
    nohup ./bin/dsdgen --overwrite --scale-factor 200 --output-location s3://tpcds-igg-test/spark-tpcds-data-200GB/ >output_200.log 2>&1 &
    nohup ./bin/dsdgen --overwrite --scale-factor 200 --partition-tables --num-partitions 1 --output-location s3://tpcds-igg-test/spark-tpcds-data-200GB-partitioned/ >output_200_p.log 2>&1 &
    nohup ./bin/dsdgen --overwrite --scale-factor 1000 --partition-tables --num-partitions 1 --output-location s3://tpcds-igg-test/spark-tpcds-data-1TB-partitioned/ >output_1000_p.log 2>&1 &