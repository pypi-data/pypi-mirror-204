import getpass, time
from aliendev_cdk.config import mongo

def check_username(username):
    client, db = mongo.connect()
    with client:
        finder = db['management'].find_one({"username":username})
        if finder:
            return finder
        else:
            return None
        
def ingest(username, password):
    client, db = mongo.connect()
    with client:
        timestamp_now = int(time.time())
        timestamp_str = str(timestamp_now)
        db['management'].insert_one({
            "_id":timestamp_str,
            "username":username,
            "password":password
        })
        print("Please wait, your accound will be already soon ⏲")
        time.sleep(2)
        if check_username(username):
            print("Congrats, your accound successfully created 🎉")
            print("Please use 'aliendev-cdk login'")
        else:
            return None    

def register():
    while True:
        username = input("Insert username: ")
        if check_username(username):
            print("username already used!")
        else:
            password = getpass.getpass("Insert password: ")
            ingest(username, password)
            break