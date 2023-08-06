import pika
import configparser
import json

def produce(queue:str, body:dict):
    config = configparser.ConfigParser()
    config.read("config.ini")

    username = config.get("RABBITMQ", "username")
    password = config.get("RABBITMQ", "password")
    host = config.get("RABBITMQ", "host")
    port = config.get("RABBITMQ", "port")
    vhost = config.get("RABBITMQ", "vhost")
    credentials = pika.PlainCredentials(username, password)
    parameters = pika.ConnectionParameters(host, port, vhost, credentials)
    
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=queue)

    channel.exchange_declare(exchange="aliendev", exchange_type="topic")
    channel.queue_bind(queue=queue, exchange="aliendev",routing_key="aliendev-route")
    channel.basic_publish(exchange="aliendev", routing_key="aliendev-route", body=json.dumps(body))
    print(f"Sent message '{json.dumps(body)}'")
