模拟上游模块importer，将数据推到对应kafka topic，isd去对应topic订阅消息，通过此方式对isd进行压测

kafkaConsumer_isd.py：消费者，从face-topic订阅消息

kafkaProducer_ftp.py：生产者，ftp方式接入face系统的数据格式

kafkaProducer_libraf.py：生产者，zmq方式接入face系统的数据格式
