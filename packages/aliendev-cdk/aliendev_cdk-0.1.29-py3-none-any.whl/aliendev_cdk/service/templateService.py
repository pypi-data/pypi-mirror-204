import os
def init(name):
    os.makedirs(name)
    os.makedirs(name+"/config")
    os.makedirs(name+"/helper")
    os.makedirs(name+"/lib")
    with open(name+"/config/__init__.py","w") as file:
        file.write(" ")