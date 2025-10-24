from kafka import KafkaConsumer, TopicPartition
import json
import configUtils
import logger

log = logger.setup_logger("kafkaUtils")
CONFIG_TOPIC_NAME = 'config'

def generateConfigFile():    
    consumer = KafkaConsumer(      
        bootstrap_servers=['rp-queue2:29092'],
        # auto_offset_reset='earliest',
        auto_offset_reset='latest',
        enable_auto_commit=False,
        # group_id='my-group',
    )

    # Assign to partition 0 (adjust if topic has multiple partitions)
    partition = TopicPartition(CONFIG_TOPIC_NAME, 0)
    consumer.assign([partition])

    # Get the latest offset
    end_offset = consumer.end_offsets([partition])[partition]

    # Seek to the last message (latest offset - 1)
    if end_offset > 0:
        consumer.seek(partition, end_offset - 1)
        for message in consumer:
            # Save message value to config.json
            log.info(f"config: {message}")
            with open(configUtils.CONFIG_FILE, 'w') as f:
                try:
                    json.dump(json.loads(message.value.decode('utf-8')), f, indent=2)
                except json.JSONDecodeError:
                    f.write(message.value.decode('utf-8'))
            print("Last message saved to config.json")
            break
    else:
        print("No messages found in topic.")

    consumer.close()

# generateConfigFile()

