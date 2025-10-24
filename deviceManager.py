import asyncio
import json
from kasa import Device
import configUtils
import logger
import genericMessageProducer
import tapo_device

ON = "on"
OFF = "off"

log = logger.setup_logger("deviceManager")

async def turn_the_device_on_or_off(alias, operation):
    log.info(f"FOR NOW: {alias}-{operation}")
    try:
        # if alias == 'Fan' or alias == 'Radiator':
        # if (alias == 'Radiator'):        
        #     await turn_the_device_on_or_tplink(alias, operation)
        # else:
        await turn_the_device_on_or_off_tapo(alias, operation)
    except Exception as e:
        error_message = f"rp-radiator. Device {alias} failed to swith {operation}. Exception: {e}"
        log.error(error_message)   
        genericMessageProducer.publish_message("error",error_message)           

async def turn_the_device_on_or_off_tapo(alias, operation):    
    ip = configUtils.getIp(alias=alias)
    
    if (len(ip.strip()) > 0):            
        client = tapo_device.get_client()
        plug = await client.p100(ip)
        if (operation == ON):                   
            await plug.on()
            log.debug("Device ON")
            genericMessageProducer.publish_message("device", f"{alias} {ON}")
        elif (operation == OFF):
            await plug.off()
            log.debug("Device OFF")
            genericMessageProducer.publish_message("device", f"{alias} {OFF}")
        else:    
            log.error("Invalid Operation Requested")
            genericMessageProducer.publish_message("error", f"Operation {operation} on {alias} FAILED")                
    else: 
        log.info("Device not found")   
        genericMessageProducer.publish_message("error",f"device {alias} not found")           

async def turn_the_device_on_or_tplink(alias, operation):
    ip = configUtils.getIp(alias=alias)
    
    if (len(ip.strip()) > 0):                    
        alias = configUtils.getAlias(ip)
        dev = await Device.connect(host = ip)                 
        if (operation == ON):                
            await dev.turn_on()
            log.debug("Device ON")
            genericMessageProducer.publish_message("device", f"{alias} {ON}")
        elif (operation == OFF):
            await dev.turn_off()
            log.debug("Device OFF")
            genericMessageProducer.publish_message("device", f"{alias} {OFF}")
        else:    
            log.error("Invalid Operation Requested")
            genericMessageProducer.publish_message("errors", f"Operation {operation} on {alias} FAILED")
        await dev.update()
    else: 
        log.info("Device not found")   
        iotgenericMessageProducerqueue.publish_message("error",f"device {alias} not found")        

# ///////////////////////////
async def get_status(alias):

    device_status = {}

    try:
        ip = configUtils.getIp(alias=alias)
        print(f"{alias} - {ip}")

        # if alias == 'Fan' or alias == 'Radiator':
        if alias == 'Radiator':
            dev = await Device.connect(host = ip)              
            device_status["device"]=alias
            state = ON if dev.state_information['State'] else OFF
            device_status["status"]=state
        elif alias == "TheHub":            
            pass            
        else:            
            client = tapo_device.get_client()
            plug = await client.p100(ip)
            device_info = await plug.get_device_info()                   
            device_status["device"]=alias             
            state = ON if device_info.device_on else OFF
            device_status["status"]=state
    except Exception as e:
        print(e)
        log.error(e)

    return device_status

async def get_devices_status():
    devices_status = []
    config = configUtils.get_config_file()        
    for alias in config.keys():
        device_status = await get_status(alias)
        devices_status.append(device_status)

    log.info(devices_status)
    genericMessageProducer.publish_message("devices-status",devices_status)

async def get_device_status(alias):
    device_status = await get_status(alias)
    log.info(device_status)
    genericMessageProducer.publish_message("device-status",device_status)    


# TODO: REMOVE ME
# asyncio.run(get_status_wrapper())  