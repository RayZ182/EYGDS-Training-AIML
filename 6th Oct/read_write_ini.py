import configparser
config = configparser.ConfigParser()

config["database"] = {
    "host" : "localhost",
    "user" : "root",
    "port" : "3307",
    "password" : "admin123"
}

# write to config file
with open('app.ini', 'w') as configfile:
    config.write(configfile)

# read from config file
config.read('app.ini')
print(config["database"]["host"])