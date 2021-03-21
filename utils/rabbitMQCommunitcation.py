import pika
import json


class rabbitConnection():
    def __init__(self):
        self.connection = None
        self.channel = None
    
    def createConnection(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='testingDetection')

    def breakConnnection(self):
        self.connection.close()
    
    def sendMessage(self, routing_key, body, exchange):
        self.channel.basic_publish(exchange=exchange,
                      routing_key=routing_key,
                      body=json.dumps(body))


rabbit = rabbitConnection()

def createConnection():
    print("Creating connection")
    rabbit.createConnection()


def breakConnection():
    print("Breaking connection")
    rabbit.breakConnection


def sendMessage(routing_key, body, exchange=''):
    rabbit.sendMessage(routing_key, body, exchange)
