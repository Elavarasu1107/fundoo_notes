from django.shortcuts import render
from .models import User
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
import logging
from rest_framework import status
from .utils import JWT
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.reverse import reverse

logging.basicConfig(filename='fundoo_note.log', encoding='utf-8', level=logging.DEBUG,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger()


class UserRegistration(APIView):
    """
    This class use to register user to the database
    """
    def post(self, request):
        """
        This method add the user to the database
        :param request: Json
        """
        try:
            serializer = RegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            token = JWT.encode({"user_id": serializer.data.get("id"), "username": serializer.data.get('username')})
            send_mail(subject="Fundoo Notes-Registration",
                      message=settings.BASE_URL + reverse('verify', kwargs={"token": token}),
                      from_email=settings.EMAIL_HOST_USER,
                      recipient_list=[serializer.data.get('email')],
                      fail_silently=False)
            return Response({"message": "Created", "status": 201, "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as ex:
            logger.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    """
    This class check the user in the database
    """
    def post(self, request):
        """
        This method use to log in the user
        :param request: Json
        """
        try:
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Login Successful", "status": 202, "data": serializer.data},
                            status=status.HTTP_202_ACCEPTED)
        except Exception as ex:
            logger.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)


class UserVerification(APIView):
    """
    This class verify the user in the database
    """
    def get(self, request, token):
        try:
            decode = JWT.decode(token)
            user = User.objects.get(username=decode.get('username'))
            if user is not None:
                user.is_verified = 1
                user.save()
                return Response({"message": "Verification Successful", "status": 202, "data": {}},
                                status=status.HTTP_202_ACCEPTED)
            return Response({"message": "Invalid User", "status": 406, "data": {}},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as ex:
            logger.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)
