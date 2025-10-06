import logging
import yaml

logging.basicConfig(format = '%(asctime)s - %(levelname)s - %(message)s',
                    filename = 'app2.log',
                    level = logging.DEBUG)

# data
config = {
    "app" :{
        "name" : "Student Portal",
        "version" : 1.0
    },
    "database" : {
        "host" : "localhost",
        "port" : 3306,
        "user" : "root"
    }
}

try:
    with open('config.yaml', 'w') as f:
        yaml.dump(config,f)
    logging.info('Created config.yaml successfully!')

    # read the config file
    with open('config.yaml' , 'r') as f:
        data = yaml.safe_load(f)
    logging.info('Config Loaded Successfully')
    logging.info('Read the yaml file')

    #printing the message
    print(f"Connecting to {data['database']['host']}:{data['database']['port']} as {data['database']['user']}")
    logging.info('Connected to database')

except FileNotFoundError as e:
    error_msg = "config.yaml file not found"
    logging.error(error_msg)
    print("Config File not Found")
