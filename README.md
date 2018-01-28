# Spark-with-Kibana-and-twitter-streaming.
Querying Data from Twitter using Twitter API Sending Data Streams into Spark and perform data processing using Spark Streaming Pushing the processed data on live Dashboard
# Real Time Data Streaming with Spark: Twitter Hashtag Count Analysis

## Project Flow
Querying Data from Twitter using Twitter API
Sending Data Streams into Spark and perform data processing using Spark Streaming
Pushing the processed data on live Dashboard

## Getting Started 
These instructions will get you a copy of the project up and running on your local machine for development purpose. See deployment for notes on how to deploy the project on a system.

### Prerequisites:   What things you need to install the software and how to install them

## Install brew and scala to fulfill the spark characteristics
## Install brew with below steps:
$ xcode-select --install
$ ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

### Installing:
## Install Scala2.11.8
$ brew install scala

##Install java to support the apache spark indtallation with java version 1.8.0_144
# Download the jre-8u65-macosx-x64.pkg file, launch th file and complete the installation

## Install Apache Spark2.2.0 for data stream processing
$ brew install apache-spark

### Make sure JDK is installed before beginning the above steps.


## Install Elasticsearch
https://www.elastic.co/guide/en/elasticsearch/reference/current/_installation.html

### View on browser
http://127.0.0.1:9200/ 


### Setup Elasticsearch
- Delete index (if already exist)
$ curl -XDELETE localhost:9200/twitter

- Create index
$ curl -XPUT 'http://127.0.0.1:9200/twitter' -d '
{
    "settings" : {
        "index" : {
            "number_of_shards" : 5, 
            "number_of_replicas" : 1 
        }
    }
}'

- Add fields mapping
$ curl -XPUT 'http://127.0.0.1:9200/twitter/_mapping/tweets' -d '
{
  "properties": {
    "count" : {
      "type" : "long"
    },
    "hashtag" : {
      "type" : "text",
      "fields" : {
        "keyword" : {
          "type" : "keyword",
          "ignore_above" : 256
        }
      }
    },
    "timestamp" : {
      "type" : "date",
      "format" : "yyyy/MM/dd HH:mm:ss"
    }
  }
}'


- Check settings and fields details of an index (open on browser)
http://127.0.0.1:9200/twitter?pretty=true

- Check data of an index (open on browser)
http://127.0.0.1:9200/twitter/_search?pretty=true

## Setup System

### Create a virtual environment
  `$ virtualenv ve --no-site-packages`
### Acrtivate virtual environment
  `$ source ve/bin/activate`
### Install pyspark (spark-2.2.0)
  `$ pip install -r REQUIREMENTS`

### Copy file elasticsearch-spark-20_2.11-5.5.0.jar in jars folder
$ cp jars/elasticsearch-spark-20_2.11-5.5.0.jar ve/lib/python/site-packages/pyspark/jars/


### Run "twitterfetch_app.py" to get tweets
$ python twitterfetch_app.py

### Run "twitterfetch_app.py" to store data in spark RDD and transfer it to elasticsearch
$ python sparkstreams_app.py

### Spark UI
http://127.0.0.1:4042/

## Install Kibana
https://www.elastic.co/downloads/kibana

### View on browser
http://127.0.0.1:5601/


##### Create various Visualizer and add them to Kibana Dashboard.
