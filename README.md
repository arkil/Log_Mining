# Project-Group-2


# Anomaly Detection as a Service



### **Team Members:**

- Ankita Chikodi                              
- Arkil Thakkar                                 
- Nehal Sharma                         
- Shravani Pande


### **Project Description:**

In our project, we aim to reduce human intervention for log file analyzing and debugging. Our methodology addresses log mining as a NLP domain problem and makes use of sophisticated techniques from natural language processing to extract key features from the logs. We are applying machine learning Random Forest Classifier to build the model. The log data that is being generated is being processed in real-time through Kafka Spark streaming pipeline. If the anomaly is detected, the system administrators are notifying about the anomalous behavior traced in the log files. Our model demonstrates an accurate predictive performance (F1-Score 93%).

### **System Architecture:**

The log data is transferred through Kafka producer which is received as a Spark streaming object. The log data in the Spark streaming object is pre-processed and applied to the pre-trained model which is build using the older logs. After pre-processing, the model will predict whether it is an anomaly and then it will send a mail to the user.

![image](https://user-images.githubusercontent.com/47070167/57565603-a8b03980-7375-11e9-9c41-86370a0de1ad.png)



### **Data Preprocessing:**

**Raw Data**

Log data generated through HDFS 

![image](https://user-images.githubusercontent.com/47070167/57565520-5884a780-7374-11e9-9dfe-9dd4e631451f.png)


**Log DataFrame**

Unstructured logs preprocessed into dataframe

![image](https://user-images.githubusercontent.com/47070167/57565523-74884900-7374-11e9-8311-9aaaf5b3e4f7.png)


**Event Sequence**

BlockID having different events 

![image](https://user-images.githubusercontent.com/47070167/57565521-6a664a80-7374-11e9-8b18-ea7ab5d0cd22.png)


**Label Dictionary**

Dictionary of blockIDs and event sequences

![image](https://user-images.githubusercontent.com/47070167/57565539-aef1e600-7374-11e9-9a77-cb7cd0b8c5a2.png)


**Label Mapping**

Mapping blockIDs with associated label i.e. Anomaly or Normal

![image](https://user-images.githubusercontent.com/47070167/57565534-a00b3380-7374-11e9-8da2-51ae87e11721.png)

### **Natural Language Processing:**
**TF-IDF**
Building matrix by converting event sequences into TF-IDF form

![image](https://user-images.githubusercontent.com/47070167/57565552-ed87a080-7374-11e9-92ae-eb77ee142aa4.png)

**Normalized Vector**

Normalizes the matrix generated from TF-IDF

![image](https://user-images.githubusercontent.com/47070167/57565561-0f812300-7375-11e9-8023-1360253fa09c.png)


### **Model Building:**
**Dumping Model**

Storing the trained model

![image](https://user-images.githubusercontent.com/47070167/57565565-2758a700-7375-11e9-991f-48f016dbf913.png)


### **Data Pipeline:**

**Kafka Logs**

Sending the kafka logs through the producer
![image](https://user-images.githubusercontent.com/47070167/57565902-908ee900-737a-11e9-8d58-2343fba31175.png)

**Processing**

The new data is sent through the Kafka producer in chunks which is received by Spark streaming object in real time. On this object, the pre-processing is performed and given to the pre-trained model which computes the label of the log. If anomaly is found, then the whole data associated with it is sent to the system administrator through e-mail.

![image](https://user-images.githubusercontent.com/47070167/57566970-6859b700-7387-11e9-9c7d-96de39dafe1e.png)


**Output:**

![image](https://user-images.githubusercontent.com/47070167/57566127-c7b2c980-737d-11e9-86ed-0b1e935b19a4.png)

### **Future Enhancement:**

- Classifying the anomalies on the basis of severity such as Critical, High, Moderate, Low.
- Alerting the different user groups according to it's criticality.
 

### **How to use this:**

- Start Zookeeper
  Open a new terminal and type zkserver

- Start Kafka Server
   Open a new terminal and type
  .\bin\windows\kafka-server-start.bat .\config\server.properties 

- Create a Kafka topic
  Open a new terminal and type
  kafka-topics.bat --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test

- Initialize a local producer 
  Open a new terminal and initialize a producer
  kafka-console-producer.bat --broker-list localhost:9092 --topic test \--new-producer < HDFS.log

- Spark 
  ./spark-submit.sh '--jars spark-streaming-kafka-0-8-assembly_2.11-2.3.3.jar pyspark-shell Spark_Log_mining.py




