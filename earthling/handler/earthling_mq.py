import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import connector.kafka_modules as km

def get_consumer(topic_name, action):
    return km.get_consumer(topic_name, action)

def produce(topic_name, message, action):
    producer = km.get_producer(action)
    producer.send(topic_name, value=message)
    producer.flush()


