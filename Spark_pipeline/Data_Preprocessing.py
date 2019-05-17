#!/usr/bin/env python
# coding: utf-8

# In[1]:


import findspark
findspark.init()


# In[2]:


from pyspark.sql import SparkSession
from pyspark.sql.functions import col


# In[8]:


from pyspark.sql import Row


# In[3]:


import pandas as pd


# In[4]:


import re


# In[ ]:


import hashlib


# In[5]:


from pyspark.sql.types import IntegerType, StringType, StructType, StructField


# In[6]:


from collections import OrderedDict


# In[7]:


spark = SparkSession.builder        .appName("LogMining")        .master("local")        .config("spark.executor.cores","6")        .config("spark.executor.memory","2g")        .getOrCreate()


# In[9]:


from pyspark.sql import Row


# In[9]:


APACHE_ACCESS_LOG_PATTERN = '^(\S+) (\S+) (\S+) (\S+) (\S+) (.*)'


# In[12]:


def parse_hdfs_log_line(logline):
    match = re.findall(APACHE_ACCESS_LOG_PATTERN, logline)
    if match is None:
        raise Error("Invalid logline: %s" % logline)
    return Row(
        Date =  match[0][0],
        Time    = match[0][1],
        Pid =   match[0][2],
        Level =  match[0][3],
        Component        = match[0][4],
        Content      = match[0][5])


# In[13]:


def parse_hdfs_file(file,APACHE_ACCESS_LOG_PATTERN, customSchema):
    parsed_file = []
    file_line = file.readlines()
    for line in range(len(file_line)):
        match = re.findall(APACHE_ACCESS_LOG_PATTERN, file_line[line])
        for mat in range(len(match)):
            bd = re.sub("[\d.-]+", "<*>", match[mat][5])
            eventid = hashlib.md5(' '.join(bd).encode('utf-8')).hexdigest()[0:8]
            parsed_file.append(Row(Date =  match[mat][0],Time = match[mat][1],Pid =match[mat][2],Level =  match[mat][3],Component   = match[mat][4],Content  = match[mat][5], EventTemplate=bd, EventId =eventid ))
    return  spark.createDataFrame(parsed_file,schema = customSchema)
    


# In[14]:


def read_file(data):
   #struct_log = spark.read.format("csv").option("header", "true").load(file)
   data_dict = OrderedDict()
   for row in data.collect():  
       blkId_list = re.findall(r'(blk_-?\d+)', row['Content'])
       blkId_set = set(blkId_list)
       for blk_Id in blkId_set:
           if not blk_Id in data_dict:
               data_dict[blk_Id] = []
           data_dict[blk_Id].append(row['EventId'])
   data_df = spark.createDataFrame(list(data_dict.items()), schema=['BlockId', 'EventSequence'])
   
   return data_df


# In[15]:


def dict_label(df_train_append, label_file):
    label_data =label_csv.toPandas().set_index('BlockId')
    label_dict = label_data['Label'].to_dict() 
    df_train_append['Label'] = df_train_append['BlockId'].apply(lambda x: 1 if label_dict[x] == 'Anomaly' else 0)
    return spark.createDataFrame(df_train_append_pd)

