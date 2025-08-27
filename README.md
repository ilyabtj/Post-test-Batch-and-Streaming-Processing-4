# Kafka + Spark Structured Streaming Pipeline

## 📌 Project Overview
This project demonstrates a **data pipeline** built with **Apache Kafka** and **Apache Spark Structured Streaming**.  
The pipeline simulates a real-time data flow starting from message generation, ingestion into Kafka, processing with Spark, and producing multiple outputs.

---

## 🔄 Pipeline Flow
1. **Data Generator** (`generator.py`)  
   - Creates nested JSON messages (user info, transaction info, and items).  

2. **Producer** (`producer.py`)  
   - Sends generated messages to Kafka topic `ilya_input`.  

3. **Consumer + Transformer** (`spark_job.py`)  
   - Reads nested JSON messages from Kafka.  
   - Flattens the structure into a tabular schema.  
   - Produces two outputs:
     - **Flattened messages** (sent back to Kafka topic `ilya_flattened`).
     - **Aggregated data** (count, sum, average transaction amounts per user).  

4. **Sink**  
   - Flattened → Kafka topic `ilya_flattened`.  
   - Aggregated → Console sink (can be extended to file or database).  

---



# How To Run
## 1. Start Kafka & Zookeeper
``` bash
docker-compose up -d
```

## 2. Run Producer (send messages)
``` bash
python app/producer.py
```

## 3. Run Spark Job (consume + transform)
``` bash
# Option 1 (if Spark is installed properly):
spark-submit app/spark_job.py

# Option 2 (via Python if pyspark installed):
python app/spark_job.py
```

## Example Outputs of Flattened Message (from topic ilya_flattened)
``` bash
{
  "user_id": 42,
  "user_name": "Ilya",
  "txn_id": 1234,
  "txn_amount": 250.0,
  "item_id": 1,
  "item_price": 75.0,
  "timestamp": "2025-08-27T10:30:00"
}
```

## Aggregated Result (console sink)
``` bash
+-------+---------+------------+----------+
|user_id|user_name|total_amount|avg_amount|
+-------+---------+------------+----------+
|42     |Ilya     |500.0       |250.0     |
|36     |Arya     |237.0       |118.5     |
```