import os
import glob
import json
from aliendev_cdk.config import rabbit
folder_name = 'helper'

class Deployment:
    def __init__(self) -> None:
        self.username = ''
        self.account_id = ''
    
    def checking_account(self):
        home_folder = os.path.expanduser("~")
        path = f'{home_folder}/.aliendev'
        if not os.path.exists(path):
            os.makedirs(path)    
            print("please login first 🥹")
        if not os.path.exists(path+"/config.json"):
            print("please login first 🥹")
        else:
            with open(path+"/config.json",'r') as file:
                json_file = json.loads(file.read())
                self.username = json_file.get('username')
                self.account_id = json_file.get('_id')
    
    def read(self):
        folder_path = ''
        for root, dirs, files in os.walk('./'):
            if folder_name in dirs:
                folder_path = os.path.join(root, folder_name)
                break
        abs_folder_path = os.path.abspath(folder_path)
        file_pattern = os.path.join(abs_folder_path, '*')
        files = glob.glob(file_pattern)
        for file in files:
            strings = {}
            file_name = file.split("/")[-1]
            with open(file, 'r') as f:
                # print(f.read())
                strings['username'] = self.username
                strings['account_id'] = self.account_id
                strings['file_name'] = file_name
                strings['data'] = f.read()
                # print(strings)
                rabbit.produce('helper',strings)