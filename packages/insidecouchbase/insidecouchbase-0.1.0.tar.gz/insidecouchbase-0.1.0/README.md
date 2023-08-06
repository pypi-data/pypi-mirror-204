# Couchbase Complete Snapshot 

![](https://upload.wikimedia.org/wikipedia/commons/6/67/Couchbase%2C_Inc._official_logo.png)

InsideCouchbase is a Python library that allows you to analyze and monitor the health of a Couchbase cluster. With InsideCouchbase, you can perform health checks on your Couchbase cluster, check for missing or corrupted data, analyze bucket usage, and monitor cluster settings.

# Features
InsideCouchbase provides the following features:

- Analyze bucket usage: You can analyze the usage of a bucket to see how much data it contains, how many items it has, and how much memory it is using.

- Check cluster health: You can perform a health check on your Couchbase cluster to see if it is functioning properly.

- Check replication status: You can check the replication status of a bucket to see if it is properly replicating data to other nodes.

- Monitor cluster settings: You can monitor the settings of your Couchbase cluster to ensure that they are properly configured.

# Getting Started

1. Install the module

```bash
pip3 install insidecouchbase
```

2. Create a simple python script/module to utilize library.

```python
import couchbase

couchbaseInstance=couchbase.couchbaseNode('127.0.0.1','Administrator','test123')
```
Example results

```
╒════╤════════════════════════════════════════════════════╤══════════╕
│    │                     Statement                      │  Result  │
╞════╪════════════════════════════════════════════════════╪══════════╡
│ 0  │      All nodes are healthy and joined cluster      │    🟢    │
├────┼────────────────────────────────────────────────────┼──────────┤
│ 1  │     All nodes using same version of Cocuhbase      │    🟢    │
├────┼────────────────────────────────────────────────────┼──────────┤
│ 2  │                 MDS model applied                  │    ❌    │
├────┼────────────────────────────────────────────────────┼──────────┤
│ 3  │  All buckets have resident ratio greater than %50  │    🟢    │
├────┼────────────────────────────────────────────────────┼──────────┤
│ 4  │ All bucket have at least 1 replica to protect data │    🟢    │
├────┼────────────────────────────────────────────────────┼──────────┤
│ 5  │        There is no missing primary vbucket         │    🟢    │
├────┼────────────────────────────────────────────────────┼──────────┤
│ 6  │          Auto-failover setting is enabled          │    ❌    │
├────┼────────────────────────────────────────────────────┼──────────┤
│ 7  │                  Cluster Score 80                  │    🟢    │
╘════╧════════════════════════════════════════════════════╧══════════╛
╒════╤═══════════════════════════════════════════════════════════════════════════════════════╤═════════════════╤═══════════════════╕
│    │                                   problemStatement                                    │   problemArea   │  problemSeverity  │
╞════╪═══════════════════════════════════════════════════════════════════════════════════════╪═════════════════╪═══════════════════╡
│ 0  │                          Autofailover setting is not enabled                          │  Configuration  │     Critical      │
├────┼───────────────────────────────────────────────────────────────────────────────────────┼─────────────────┼───────────────────┤
│ 1  │ The node has multiple couchbase services.For production MDS model should be followed. │ 172.17.0.6:8091 │      Medium       │
╘════╧═══════════════════════════════════════════════════════════════════════════════════════╧═════════════════╧═══════════════════╛
-- Details -- 
+----+-----------------+-----------------+---------------+-------------------+-----------------------+
|    | nodeIP          | clusterMember   | healtStatus   | services          | couchbaseVersion      |
|----+-----------------+-----------------+---------------+-------------------+-----------------------|
|  0 | 172.17.0.2:8091 | active          | healthy       | ['kv']            | 7.1.3-3479-enterprise |
|  1 | 172.17.0.3:8091 | active          | healthy       | ['kv']            | 7.1.3-3479-enterprise |
|  2 | 172.17.0.4:8091 | active          | healthy       | ['index']         | 7.1.3-3479-enterprise |
|  3 | 172.17.0.5:8091 | active          | healthy       | ['n1ql']          | 7.1.3-3479-enterprise |
|  4 | 172.17.0.6:8091 | active          | healthy       | ['index', 'n1ql'] | 7.1.3-3479-enterprise |
+----+-----------------+-----------------+---------------+-------------------+-----------------------+
+----+--------------+-----------------------+--------------+------------------+-------------------------+-------------------+-----------------------+---------------------+
|    | bucketName   |   primaryVbucketCount | bucketType   |   bucketReplicas |   bucketQuotaPercentage |   bucketItemCount |   bucketResidentRatio |   bucketDisUsedInMb |
|----+--------------+-----------------------+--------------+------------------+-------------------------+-------------------+-----------------------+---------------------|
|  0 | beer-sample  |                  1024 | membase      |                1 |                    16.5 |              3711 |                   100 |                46.7 |
+----+--------------+-----------------------+--------------+------------------+-------------------------+-------------------+-----------------------+---------------------+
+----+------------+--------------------+--------------+
|    | xdcrName   | xdcrConnectivity   | targetNode   |
|----+------------+--------------------+--------------|
|  0 | test       | RC_OK              | 172.17.0.7   |
+----+------------+--------------------+--------------+

+----+-----------------+----------+
|    | configName      |   status |
|----+-----------------+----------|
|  0 | autofailover    |    False |
|  1 | email-alerting  |    False |
|  2 | auto-compaction |       30 |
+----+-----------------+----------+

```

# Supported Couchbase Version

- Couchbase 7.0.X
- Couchbase 7.1.X

# Contributing

If you would like to contribute to InsideCouchbase, please submit a pull request with your changes. Before submitting a pull request, please make sure that your changes are properly tested and documented.

# License
InsideCouchbase is licensed under the MIT license. See the LICENSE file for more information.

