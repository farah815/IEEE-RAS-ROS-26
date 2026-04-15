import json
def load_or_create_config():
    try:
         with open  ("configg.json" , "r") as file :
            data=json.load(file)

    except FileNotFoundError :
         default_config = {
            "mode": "normal",
            "version": 1.0,
            "debug": False
        }
         
         with open ("configg.json" , "w") as file :
             json.dump(default_config,file)
             print("Config file created. System Ready.")
             return default_config
         
load_or_create_config()