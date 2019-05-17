#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import findspark
findspark.init()


# In[ ]:


from pyspark.sql import SparkSession
from pyspark.sql.functions import col


# In[ ]:


import pandas as pd


# In[ ]:


import pandas as pd


# In[ ]:


from pyspark.sql.types import IntegerType, StringType, StructType, StructField


# In[ ]:


from Data_Preprocessing import parse_hdfs_log_line, parse_hdfs_file, read_file, dict_label


# In[ ]:


from Extractor import FeatureExtractor


# In[ ]:


from collections import OrderedDict


# In[ ]:


spark = SparkSession.builder        .appName("LogMining")        .master("local")        .config("spark.executor.cores","6")        .config("spark.executor.memory","2g")        .getOrCreate()


# In[ ]:


APACHE_ACCESS_LOG_PATTERN = '^(\S+) (\S+) (\S+) (\S+) (\S+) (.*)'


# In[ ]:


fo = open("Train.log", "r")


# In[ ]:


customSchema = StructType([
    StructField("Date", StringType(), True),
    StructField("Time", StringType(), True),
    StructField("Pid", StringType(), True),
    StructField("Level", StringType(), True),
    StructField("Component", StringType(), True),
    StructField("Content", StringType(), True),
    StructField("EventTemplate", StringType(), True),
    StructField("EventId", StringType(), True)
    
])


# In[ ]:


parsed_file = parse_hdfs_file(fo,APACHE_ACCESS_LOG_PATTERN,customSchema )


# In[ ]:


df_train_append = read_file(df_train)


# In[ ]:


label_csv = pd.read_csv('anomaly.csv')


# In[ ]:


df_event = dict_label(df_train_append,label_csv )


# In[ ]:


from sklearn.model_selection import train_test_split


# In[ ]:


x_train, x_test, y_train, y_test = train_test_split(df_train_append['EventSequence'].values, df_train_append['Label'].values, test_size = 0.2)


# In[ ]:


from collections import Counter
from scipy.special import expit
from itertools import compress


# In[ ]:


feature_extractor = FeatureExtractor()
x_train = feature_extractor.fit_transform(x_train, term_weighting='tf-idf')
x_test = feature_extractor.transform(x_test)


# In[ ]:


from sklearn.ensemble import RandomForestClassifier

rfclf = RandomForestClassifier(max_depth=1, random_state=42)
rfclf = rfclf.fit(x_train, y_train)

from sklearn.metrics import f1_score

predicted_y = rfclf.predict(x_test)
print("test accuracy: ",f1_score(y_test, predicted_y, average='micro'))


# In[ ]:


from sklearn.externals import joblib  

joblib.dump(rfclf, "nlp-trained-model.pkl")


# In[ ]:




