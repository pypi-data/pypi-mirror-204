import os

def logout():
    home_folder = os.path.expanduser("~")
    path = f'{home_folder}/.aliendev'
    if os.path.exists(path+"/config.json"):
        os.remove(path+"/config.json")
        print("Logout Successfully 😢")
    else:
        print("You has already logout 😇")