from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.reverse import reverse
import logging
from time import sleep

logging.basicConfig(filename='fundoo_note.log', encoding='utf-8', level=logging.DEBUG,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger()


@shared_task()
def email_sender(token, recipient):
    try:
        sleep(10)
        send_mail(subject='Fundoo Notes Registration Celery',
                  message=settings.BASE_URL + reverse('verify', kwargs={"token": token}),
                  from_email=None,
                  recipient_list=[recipient])
    except Exception as ex:
        logger.exception(ex)
