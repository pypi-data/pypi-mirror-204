import os, getpass, json
from aliendev_cdk.config import mongo

def check_login(username, password):
    client, db = mongo.connect()
    with client:
        finder = db['management'].find_one({"$and":[{"username":username},{"password":password}]})
        if finder:
            return finder
        else:
            return None

def login():
    home_folder = os.path.expanduser("~")
    path = f'{home_folder}/.aliendev'
    if not os.path.exists(path):
        os.makedirs(path)    
        print("folder created")
    if not os.path.exists(path+"/config.json"):
        while True:
            username = input("Insert username: ")
            password = getpass.getpass("Insert password: ")
            data = check_login(username, password)
            if data is not None:
                with open(path+"/config.json","w") as files:
                    json.dump(data, files, indent=4)
                    print("Login has been succesfully 🎉")
                break
            else:
                print("Your identity has been invalid")
                reinsert = input("Insert again?[y/n] = ")
                if reinsert.lower() == "n":
                    break
    else:
        print("You already login 🎉")
    