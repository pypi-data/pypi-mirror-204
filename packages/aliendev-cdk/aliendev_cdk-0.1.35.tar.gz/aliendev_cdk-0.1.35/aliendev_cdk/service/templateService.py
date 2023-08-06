import os
import shutil


def init(name):
    os.makedirs(name)
    os.makedirs(name+"/config")
    os.makedirs(name+"/helper")
    os.makedirs(name+"/lib")
    shutil.copy2('service/template/helper/test_get.py', name+"/helper/")
    shutil.copy2('service/template/helper/test_post.py', name+"/helper/")
    shutil.copy2('service/template/lib/stack.py', name+"/lib/")
    shutil.copy2('service/template/README.md', name+"/")

    # with open(name+"/helper/test_get.py","w") as file:
    #     file.write("def handler(event:dict):\n")
    #     file.write("\treturn event")
    
    # with open(name+"/helper/test_post.py","w") as file:
    #     file.write("def handler(event:dict):\n")
    #     file.write("\tevents = event.copy()\n")
    #     file.write("\tevents['_id'] = 1\n")
    #     file.write('\treturn {"statusCode":200,"message":"success","data":events}\n')
        
    # with open(name+"/lib/stack.py","w") as file:
    #     file.write("from aliendev_api import ApiGateway\n\n")
    #     file.write('api = ApiGateway("username", "Test API")')
    #     file.write('\nparam = [[{"key": "name","data_type": "string","required": True},{"key": "age","data_type": "int","required": False}]]\n')
    #     file.write('\napi.addMethod(method="GET", prefix="/test-get",param_type="param", data=param)')
    #     file.write('\napi.addMethod(method="POST", prefix="/test-post",param_type="body", data=param)')
    #     file.write('\napi.build()')
        