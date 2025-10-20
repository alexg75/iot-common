from json import dumps
from kafka import KafkaProducer
import logger

TOPIC_NAME = 'social-message'
log = logger.setup_logger("message-producer")

def publish_message(message):
    try:
        producer = KafkaProducer(bootstrap_servers=['rp-queue2:29092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
        producer.send(str(TOPIC_NAME), value=message)
        log.info(f"MESSAGE {message} sent to {TOPIC_NAME}")
    except:
        log.error(f"MESSAGE {message} not sent to {TOPIC_NAME}")


