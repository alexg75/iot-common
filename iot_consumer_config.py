import asyncio
from kafka import KafkaConsumer
from json import loads
import logger
import configUtils

log = logger.setup_logger("iot_consumer_congig")

TOPIC_NAME = "config"

async def main():
    log.info("Comsumer Action started")    
    consumer = KafkaConsumer(
        TOPIC_NAME,        
        bootstrap_servers=['rp-queue2:29092'],
        # auto_offset_reset='earliest',
        auto_offset_reset='latest',
        enable_auto_commit=True,
        # group_id='my-group',
        value_deserializer=lambda x: loads(x.decode('utf-8')))

    for message in consumer:
        message = message.value
        log.info(f"config values: {message}")
        configUtils.persist_config_as_json(message)
        

asyncio.run(main())