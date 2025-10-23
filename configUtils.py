import json
import logger


CONFIG_FILE = "/iot/config.json"
log = logger.setup_logger("configUtils")


def persist_config_as_json(alias_to_ip):
    with open(CONFIG_FILE, "w") as outfile: 
        json.dump(alias_to_ip, outfile)

def get_config_file():
    with open(CONFIG_FILE) as config_json:
        return json.load(config_json)        
    
    return "Configuration not retrieved"

def getIp(alias):
    with open(CONFIG_FILE) as config_json:
        config_dict = json.load(config_json)
    return config_dict[alias]


# {"Garage": "192.168.178.22", "Conservatory": "192.168.178.23"}
def getAlias(ip):
    with open(CONFIG_FILE) as config_json:
        config_dict = json.load(config_json)
        for alias in config_dict.keys():            
            myIp = config_dict[alias]
            if (myIp == ip):
                return alias
        log.error(f"Cannot find a alias for IP: {ip}")
        raise Exception(f"Cannot find a alias for IP: {ip}") 