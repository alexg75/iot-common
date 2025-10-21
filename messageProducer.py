from json import dumps
from kafka import KafkaProducer
import logger
from socialMessageUtils import addSlackChannel

TOPIC_NAME = 'social-message'
log = logger.setup_logger("message-producer")

def publish_message(slack_channel, message):
    try:
        producer = KafkaProducer(bootstrap_servers=['rp-queue2:29092'],value_serializer=lambda x: dumps(x).encode('utf-8'))

        log.info(f"message {message}")
        formattedMessage = addSlackChannel(slack_channel, message)        
        log.info(f"formatted message {formattedMessage}")
        
        producer.send(str(TOPIC_NAME), value=formattedMessage)
        log.info(f"MESSAGE {message} sent to queue {TOPIC_NAME} and slack channel {slack_channel}")
    except Exception as e:
        log.error(f"MESSAGE {message} not sent to queue {TOPIC_NAME} and slack channe {slack_channel}")
        log.error(e)


