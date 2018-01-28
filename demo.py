from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
conf = SparkConf()
conf.set("es.nodes", "127.0.0.1:9200")

sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)
df = sqlContext.read.option("es.resource", "test-index").format("org.elasticsearch.spark.sql").load()
df.show()


#df.write.save("test-index", format="org.elasticsearch.spark.sql")