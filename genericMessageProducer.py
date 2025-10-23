from json import dumps
from kafka import KafkaProducer
import logger

log = logger.setup_logger("genericProducer")

def publish_message(topic, message):
    try:
        producer = KafkaProducer(bootstrap_servers=['rp-queue2:29092'],value_serializer=lambda x: dumps(x).encode('utf-8'))        
        formattedMessage = formatMessage(message)
        producer.send(str(topic), value=formattedMessage)
        log.info(f"MESSAGE {message} sent to {topic}")
    except:
        log.error(f"MESSAGE {message} not sent to {topic}")


def formatMessage(message):
    return {
        "message": message
    }