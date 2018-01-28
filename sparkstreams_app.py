#Importing Spark libraries 
import sys
from datetime import datetime

from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import Row, SQLContext


URL = '127.0.0.1:9200'
INDEX = 'twitter'
TYPE = 'tweets'
RESOURCE = '%s/%s' % (INDEX, TYPE)


# Creating Spark Configuration 
conf = SparkConf()
conf.setAppName("TwitterStreamApp")
conf.set('es.nodes', URL)
conf.set('es.index.auto.create', 'true')

# Create Spark instance with the above spark configuration
spc = SparkContext(conf=conf)
spc.setLogLevel("ERROR")

# Create the Streaming Context from the spark context created above with window size 2 seconds
spsc = StreamingContext(spc, 2)

# Setting a checkpoint to allow RDD recovery in case of node unavailability
spsc.checkpoint("checkpoint_TwitterApp")

# Read data from port 9009 on localhost
dataStream = spsc.socketTextStream("localhost", 9009)


def aggr_tags_count(new_values, total_sum):
    '''
    The function 'aggr_tags_count' aggregates and sum up the hashtag counts
    collected for each category
    '''
    return sum(new_values) + (total_sum or 0)

def get_sqlcontext_instance(spark_context):
    '''
    Create sql context object globally (singleton object)
    '''
    if 'sqlContextSingletonInstance' not in globals():
        globals()['sqlContextSingletonInstance'] = SQLContext(spark_context)
    return globals()['sqlContextSingletonInstance']

def send_dataframe_to_elasticsearch(df):
    '''
    Send data frames to elesticsearch
    '''
    df.write.format('org.elasticsearch.spark.sql').mode('overwrite').save(RESOURCE)

def rdd_process(time, rdd):
    print("~~~~~~~~~~~~~~ %s ~~~~~~~~~~~~~~" % str(time))
    try:
        # Get spark sql singleton context from the current context
        sql_context = get_sqlcontext_instance(rdd.context)
        # convert the RDD to Row RDD
        row_rdd = rdd.map(lambda w: Row(
            hashtag=w[0], count=w[1], timestamp=datetime.now().strftime('%Y/%m/%d %H:%M:%S')))
        if row_rdd.isEmpty():
            print('RDD is empty')
        else:
            # create a DF from the Row RDD
            hashtags_df = sql_context.createDataFrame(row_rdd)
            # Register the dataframe as table
            hashtags_df.registerTempTable("hashtags")
            # get the top 10 hashtags from the table using SQL and print them
            hashtag_counts_dataf = sql_context.sql(
                "select hashtag, count, timestamp  from hashtags order by count desc limit 10")
            hashtag_counts_dataf.show()
            # call this method to send them to elasticsearch
            send_dataframe_to_elasticsearch(hashtags_df)
    except:
        e = sys.exc_info()
        print("Error: %s" % e[0])

# split each tweet into individual words to create category
words = dataStream.flatMap(lambda line: line.split(" "))
# filter the words to get only hashtags from tweets, then to map each hashtag to be paired of with (hashtag,1)
hashtags = words.filter(lambda w: '#' in w).map(lambda x: (x, 1))
# Sum up each of the count of hashtag to its last count
tags_totals = hashtags.updateStateByKey(aggr_tags_count)
# Perform processing for each RDD generated in each interval
tags_totals.foreachRDD(rdd_process)

# start the streaming computation
spsc.start()
# wait for the streaming to finish
spsc.awaitTermination()
