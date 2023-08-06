from aliendev_api import ApiGateway

api = ApiGateway("username", "Test API")
param = [[{"key": "name","data_type": "string","required": True},{"key": "age","data_type": "int","required": False}]]

api.addMethod(method="GET", prefix="/test-get",param_type="param", data=param)
api.addMethod(method="POST", prefix="/test-post",param_type="body", data=param)
api.build()