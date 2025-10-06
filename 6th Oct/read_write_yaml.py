import yaml

#data
config = {
    "model" : "RandomForest",
    "params" :{
        "n_estimators" : 100,
        "max_depth" : 5
    },
    "dataset" : "student.csv"
}

#write to yaml file
with open('config.yaml','w') as f:
    yaml.dump(config,f)

# read from yaml file
with open('config.yaml', 'r') as f:
    data = yaml.safe_load(f)

# using data from yaml file
print(f"The number of estimators in the {data['model']} are {data['params']['n_estimators']}")
