#!/usr/bin/env python
import pika
import logging
import json
import smtplib
import ssl
from email.message import EmailMessage
from dotenv import load_dotenv
from os import environ

logging.basicConfig(filename='fundoo_note.log', encoding='utf-8', level=logging.ERROR,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger()
load_dotenv()


class Consumer:

    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='send_email')
        self.sender = environ.get('EMAIL_HOST_USER')
        self.sender_password = environ.get('EMAIL_HOST_PASSWORD')

    def callback(self, ch, method, properties, body):
        try:
            payload = json.loads(body.decode('UTF-8'))
            msg = EmailMessage()
            msg['From'] = self.sender
            msg['To'] = payload.get('recipient')
            msg['Subject'] = 'Rabbit Fundoo Notes Registration'
            msg.set_content(payload.get('message'))
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(user=self.sender, password=self.sender_password)
                smtp.sendmail(self.sender, payload.get('recipient'), msg.as_string())
                print("[*] Mail sent to ", payload.get('recipient'))
                smtp.quit()
        except Exception as ex:
            logger.exception(ex)

    def receiver(self):
        self.channel.basic_consume(queue='send_email', on_message_callback=self.callback, auto_ack=True)
        print(' [*] Receive Server Started. To exit press CTRL+C')
        self.channel.start_consuming()


if __name__ == '__main__':
    try:
        consumer = Consumer()
        consumer.receiver()
    except KeyboardInterrupt:
        print("Connection closed")
