import pika
import json

def produce(queue:str, body:dict):
    username = 'guest'
    password = 'guest'
    host = '203.194.113.203'
    port = '5672'
    vhost = '/'
    credentials = pika.PlainCredentials(username, password)
    parameters = pika.ConnectionParameters(host, port, vhost, credentials)
    
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=queue)

    channel.exchange_declare(exchange="aliendev", exchange_type="topic")
    channel.queue_bind(queue=queue, exchange="aliendev",routing_key="aliendev-route")
    channel.basic_publish(exchange="aliendev", routing_key="aliendev-route", body=json.dumps(body))
    # print(f"Sent message '{json.dumps(body)}'")
    print("Your engine has deployed 😀")
