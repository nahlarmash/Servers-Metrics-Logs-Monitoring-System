<h1 align="center">
Servers Metrics & Logs Monitoring System

## Project Overview
This project simulates a real-time monitoring system for a cluster of 10 cloud storage servers and a load balancer. Each server sends system metrics, while the load balancer agent emits access logs. The system ingests, processes, and stores this data using:

- **Apache Kafka** (3 brokers).

- **PostgreSQL** for storing metrics.

- **Apache Spark** + **Hadoop** HDFS for log analytics.

- **Docker Compose** for managing the whole stack.

## Architecture
![Server_Metrics_Logs_Pipeline](https://github.com/nahlarmash/Servers-Metrics-Logs-Monitoring-System/blob/main/Server_Metrics_Logs_Pipeline.png)

## Components
- **Kafka Cluster:**
  - 3 brokers + Zookeeper.

- **Topics created:**

  - test-topic3: Load balancer logs.

  - test-topic4: Server metrics.

- **Java Producers:**
Provided Maven-based Java project simulates:

   - logs.

   - metrics (CPU, memory, etc.).

- **Python Kafka Consumer:**
Parses and stores server metrics in PostgreSQL.

- **Spark Streaming App:**
Stores output as Parquet files in HDFS.

- **Hadoop:**
Namenode + (2) Datanodes.

## Secrets & Environment Variables
- All secrets like pgAdmin & database passwords are managed via a `.env` file and loaded securely by services like PostgreSQL, Python consumer, and pgAdmin.
- You will create `.env` file in the project directory, then you will write passwords in the file like this:
```
POSTGRES_USER=postgres_user
POSTGRES_PASSWORD=postgres_password
POSTGRES_DB=postgres_db
POSTGRES_HOST=postgres_host

PGADMIN_DEFAULT_EMAIL=your_email_here
PGADMIN_DEFAULT_PASSWORD=your_password_here
```

## Setup Instructions  
### 1. Clone the Repository  
clone the repository or download it to your local machine.

### 2.Generate JAR File
In this step you should have Apache Maven in your system, Then run:
```
cd java-producer
mvn clean package
```
This will generate a JAR file inside `target/`.

### 2.Run the Project Using Docker
```
docker-compose up -d --build
```
- Wait for services to initialize.
- Once containers are up, immediately run the following HDFS commands in terminal:
```
docker exec -it hadoop-namenode hdfs dfs -mkdir -p /user/spark
docker exec -it hadoop-namenode hdfs dfs -chown -R spark:spark /user/spark
```
##  Access the Results
- **Kafka UI** (check topic messages):
http://localhost:8083

- **pgAdmin** (inspect metrics in PostgreSQL):
create .env file in your directory then access:
http://localhost:8085

- **HDFS UI** (see Spark logs output in /user/spark/):
http://localhost:9870
