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

## 🗂 Project Structure


