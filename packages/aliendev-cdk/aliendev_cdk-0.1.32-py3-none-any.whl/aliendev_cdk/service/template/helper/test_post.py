def handler(event:dict):
	events = event.copy()
	events['_id'] = 1
	return {"statusCode":200,"message":"success","data":events}
