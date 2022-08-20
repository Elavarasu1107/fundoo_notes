from django.shortcuts import render
from django.http import JsonResponse
from .models import User
from django.contrib.auth import authenticate
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
            User.objects.create_user(**data)
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
            user = authenticate(username=data.get('username'), password=data.get('password'))
            if user is not None:
                return JsonResponse({"message": "User Login Successful"})
            return JsonResponse({"message": "Invalid Credentials"})
        return JsonResponse({"message": "Invalid Request"})
    except Exception as ex:
        logger.exception(ex)
        return JsonResponse({"message": ex})
