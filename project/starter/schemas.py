from pyspark.sql.types import StructField, StructType, StringType, BooleanType, ArrayType, DateType, FloatType

# TODO: create a StructType for the Kafka redis-server topic which has all changes made to Redis - before Spark 3.0.0, schema inference is not automatic
redisSchema = StructType([
    StructField('key', StringType()),
    StructField('value', StringType()),
    StructField('expiredType', StringType()),
    StructField('expiredValue', StringType()),
    StructField('existType', StringType()),
    StructField('ch', StringType()),
    StructField('incr', BooleanType()),
    StructField('zSetEntries', ArrayType(
        StructType([
            StructField('element', StringType()),
            StructField('score', StringType())
        ]))
                )
])

# TODO: create a StructType for the Customer JSON that comes from Redis- before Spark 3.0.0, schema inference is not automatic
# Example
# {
#   "customerName": "Sam Test",
#   "email": "sam.test@test.com",
#   "phone":"8015551212",
#   "birthDay":"2001-01-03"
# }
customerSchema = StructType([
    StructField('customerName', StringType()),
    StructField('email', StringType()),
    StructField('phone', StringType()),
    StructField('birthDay', StringType())
])

# TODO: create a StructType for the Kafka stedi-events topic which has the Customer Risk JSON that comes from Redis- before Spark 3.0.0, schema inference is not automatic
# Example
# {
#   "customer":"Jason.Mitra@test.com",
#   "score":7.0,
#   "riskDate":"2020-09-14T07:54:06.417Z"
# }
stediEventSchema = StructType([
    StructField('customer', StringType()),
    StructField('score', FloatType()),
    StructField('riskDate', DateType())
])