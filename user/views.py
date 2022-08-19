from django.shortcuts import render
from django.http import JsonResponse
from .models import User
import json
import logging

logging.basicConfig(filename='fundoo_note.log', encoding='utf-8', level=logging.DEBUG,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger()


def user_registration(request):
    """
    This function add the user to the database
    """
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            User.objects.create(username=data.get('user_name'), email=data.get('email'),
                                password=data.get('password'), phone=data.get('phone'),
                                location=data.get('location'))
            return JsonResponse({"message": "User added Successfully"})
        return JsonResponse({"message": "Invalid Request"})
    except Exception as ex:
        logger.exception(ex)
        return JsonResponse({"message": ex})


def user_login(request):
    """
    This function checks the user in the database
    """
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            user_object = User.objects.filter(username=data.get('username'))
            user_data = user_object.first()
            if user_data.username == data.get('username') and user_data.password == data.get('password'):
                return JsonResponse({"message": "User Login Successful"})
            return JsonResponse({"message": "Invalid Credentials"})
        return JsonResponse({"message": "Invalid Request"})
    except Exception as ex:
        logger.exception(ex)
        return JsonResponse({"message": ex})
