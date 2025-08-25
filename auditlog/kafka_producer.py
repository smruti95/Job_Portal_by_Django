import os
from kafka import KafkaProducer
import json

# Detect if running inside Docker (you can set this env var in docker-compose)
if os.getenv('DOCKER_ENV') == '1':
    KAFKA_BROKER_URL = 'kafka:9092'  
else:
    KAFKA_BROKER_URL = 'localhost:19092'  

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER_URL,
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    api_version=(7, 4, 0),  
)

def publish_audit_log(data: dict):
    """
    Publish the audit log dictionary to Kafka topic 'audit-logs'
    """
    producer.send('audit-logs', value=data)
    producer.flush()
