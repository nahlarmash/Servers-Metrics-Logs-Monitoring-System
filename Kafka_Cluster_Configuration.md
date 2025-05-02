<h1 align="center">
Kafka Cluster: Broker & Topic Configuration

## Kafka Cluster Overview 
- The Kafka cluster in this project consists of: 
  - 1 Zookeeper node (for coordination) 
  - 3 Kafka brokers (to distribute and replicate messages) 

- Broker Configuration 
Each broker is a separate container, running on its own port. Below are the basic details: 
- Broker 1 
     - Container name: kafka-1 
     - Broker ID: 1 
     - Port: 29091 
     - Advertised Listeners: 
       - Internal: PLAINTEXT://kafka-1:9092 
       - External: PLAINTEXT_HOST://localhost:29091 
- Broker 2 
     - Container name: kafka-2 
     - Broker ID: 2 
     - Port: 29092 
     - Advertised Listeners: 
       - Internal: PLAINTEXT://kafka-2:9093 
       - External: PLAINTEXT_HOST://localhost:29092 
- Broker 3 
     - Container name: kafka-3 
     - Broker ID: 3 
     - Port: 29093 
     - Advertised Listeners: 
       - Internal: PLAINTEXT://kafka-3:9094 
       - External: PLAINTEXT_HOST://localhost:29093 

- All brokers connect to the same Zookeeper at zookeeper:2181. 
- Topic auto-creation is disabled to ensure manual topic management. 

## Topics Configuration 
Two Kafka topics are manually created using an initialization container: 
- Topic 1: test-topic3 
    - Purpose: Stores logs from the load balancer 
    - Producer: Java application 
    - Replication factor: 3 
    - Partitions: 1 
- Topic 2: test-topic4 
    - Purpose: Stores metrics from 10 servers (CPU, memory, etc.) 
    - Producer: Java application  
    - Replication factor: 3 
    - Partitions: 1 

## Monitoring 
You can view brokers and topics using Kafka UI at: 
http://localhost:8083