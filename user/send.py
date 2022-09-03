#!/usr/bin/env python
import pika
import json


class Producer:

    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='send_email')

    def publish(self, method, payload):
        payload_bytes = json.dumps(payload).encode('UTF-8')
        self.channel.basic_publish(exchange='',
                                   routing_key='send_email',
                                   body=payload_bytes,
                                   properties=pika.BasicProperties(method))
        self.connection.close()
