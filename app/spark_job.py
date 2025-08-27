from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, from_json, sum as _sum, avg
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, ArrayType

# 1. Spark Session
spark = SparkSession.builder \
    .appName("KafkaSparkPipeline") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# 2. Schema untuk nested JSON
schema = StructType([
    StructField("user", StructType([
        StructField("id", IntegerType()),
        StructField("name", StringType())
    ])),
    StructField("transaction", StructType([
        StructField("id", IntegerType()),
        StructField("amount", DoubleType()),
        StructField("items", ArrayType(
            StructType([
                StructField("item_id", IntegerType()),
                StructField("price", DoubleType())
            ])
        ))
    ])),
    StructField("timestamp", StringType())
])

# 3. Read from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "ilya_input") \
    .load()

parsed = df.selectExpr("CAST(value AS STRING) as json") \
    .select(from_json(col("json"), schema).alias("data")) \
    .select("data.*")

# 4. Flatten (output 1)
flattened = parsed.select(
    col("user.id").alias("user_id"),
    col("user.name").alias("user_name"),
    col("transaction.id").alias("txn_id"),
    col("transaction.amount").alias("txn_amount"),
    explode("transaction.items").alias("item"),
    col("timestamp")
).select(
    "user_id", "user_name", "txn_id", "txn_amount",
    col("item.item_id").alias("item_id"),
    col("item.price").alias("item_price"),
    "timestamp"
)

# 5. Aggregation (output 2)
agg = flattened.groupBy("user_id", "user_name") \
    .agg(
        _sum("txn_amount").alias("total_amount"),
        avg("txn_amount").alias("avg_amount")
    )

# 6. Write sinks
# Sink 1: Flattened back to Kafka
flattened_json = flattened.selectExpr("to_json(struct(*)) as value")

flattened_query = flattened_json.writeStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("topic", "ilya_flattened") \
    .option("checkpointLocation", "/tmp/checkpoint_flattened") \
    .start()

# Sink 2: Aggregated to console (or file/db)
agg_query = agg.writeStream \
    .outputMode("complete") \
    .format("console") \
    .option("truncate", "false") \
    .start()

spark.streams.awaitAnyTermination()
