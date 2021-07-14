from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, unbase64, base64, split
from constants import KAFKA_BROKERS_STRING, STEDI_EVENTS_TOPIC
from schemas import stediEventSchema

spark = SparkSession.builder.appName('STEDI-events').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

# TODO: using the spark application object, read a streaming dataframe from the Kafka topic stedi-events as the source
# Be sure to specify the option that reads all the events from the topic including those that were published before you started the spark stream
stediEventsRawDf = spark.readStream\
    .format('kafka')\
    .option('subscribe', STEDI_EVENTS_TOPIC)\
    .option('kafka.bootstrap.servers', KAFKA_BROKERS_STRING)\
    .option('startingOffsets', 'earliest')\
    .load()

# TODO: cast the value column in the streaming dataframe as a STRING
stediEventsDf = stediEventsRawDf.select('cast(value as string) value')

# TODO: parse the JSON from the single column "value" with a json object in it, like this:
# +------------+
# | value      |
# +------------+
# |{"custom"...|
# +------------+
#
# and create separated fields like this:
# +------------+-----+-----------+
# |    customer|score| riskDate  |
# +------------+-----+-----------+
# |"sam@tes"...| -1.4| 2020-09...|
# +------------+-----+-----------+
#
# storing them in a temporary view called CustomerRisk
stediEventsDf.withColumn('value', from_json('value', stediEventSchema))\
    .select(col('value.*'))\
    .createOrReplaceTempView('CustomerRisk')

# TODO: execute a sql statement against a temporary view, selecting the customer and the score from the temporary view, creating a dataframe called customerRiskStreamingDF
customerRiskStreamingDf = spark.sql('SELECT customer, score FROM CustomerRisk')

# TODO: sink the customerRiskStreamingDF dataframe to the console in append mode
# 
# It should output like this:
#
# +--------------------+-----
# |customer           |score|
# +--------------------+-----+
# |Spencer.Davis@tes...| 8.0|
# +--------------------+-----
# Run the python script by running the command from the terminal:
# /home/workspace/submit-event-kafka-streaming.sh
# Verify the data looks correct
