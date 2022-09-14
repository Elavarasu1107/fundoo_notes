from django.shortcuts import render
from .models import User
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
import logging
from rest_framework import status
from .utils import JWT, TokenRole
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.reverse import reverse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .utils import verify_token

logging.basicConfig(filename='fundoo_note.log', encoding='utf-8', level=logging.DEBUG,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger()


class UserRegistration(APIView):
    """
    This class use to register user to the database
    """
    @swagger_auto_schema(operation_summary='Register User', request_body=RegisterSerializer)
    def post(self, request):
        """
        This method add the user to the database
        :param request: Json
        """
        try:
            serializer = RegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            token = JWT.encode({"user_id": serializer.data.get("id"), "username": serializer.data.get('username'),
                                "role": TokenRole.verify_user.value})
            send_mail(subject="Fundoo Notes-Registration",
                      message=settings.BASE_URL + reverse('verify', kwargs={"token": token}),
                      from_email=None,
                      recipient_list=[serializer.data.get('email')])
            return Response({"message": "Created", "status": 201, "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as ex:
            logger.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    """
    This class check the user in the database
    """
    @swagger_auto_schema(operation_summary='Login User', request_body=LoginSerializer)
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
    @swagger_auto_schema(operation_summary='Verify User')
    def get(self, request, token):
        try:
            decode = JWT.decode(token)
            if decode.get('role') != TokenRole.verify_user.value:
                raise Exception("Invalid token role")
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


class ChangePassword(APIView):
    """
    This class allows to change password after login by user
    """
    @verify_token
    def post(self, request):
        try:
            user = User.objects.get(id=request.data.get('user'))
            if not user or not user.check_password(request.data.get('old_password')):
                raise Exception('user and password does not match')
            user.set_password(request.data.get('new_password'))
            user.save()
            return Response({"message": "Password Changed Successfully", "status": 202, "data": {}},
                            status=status.HTTP_202_ACCEPTED)
        except Exception as ex:
            logger.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)


class ForgotPassword(APIView):
    """
    This class allows user to reset password if user forgot the password
    """
    def post(self, request):
        try:
            user = User.objects.get(username=request.data.get('username'), email=request.data.get('email'))
            if not user:
                raise Exception('user and email does not match')
            token = JWT.encode({"username": request.data.get('username'), "email": request.data.get('email'),
                                "role": TokenRole.forgot_password.value})
            send_mail(subject='Fundoo Notes Forgot Password',
                      from_email=None,
                      message=settings.BASE_URL + reverse('verify_forgot_password', kwargs={"token": token}),
                      recipient_list=[request.data.get('email')])
            return Response({"message": "Email sent successfully", "status": 200, "data": {}},
                            status=status.HTTP_200_OK)
        except Exception as ex:
            logger.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)


class VerifyForgotPassword(APIView):
    """
    This class verifies the link sent to the user's email for resetting password
    """
    def post(self, request, token):
        try:
            decode = JWT.decode(token)
            if decode.get('role') != TokenRole.forgot_password.value:
                raise Exception("Invalid token role")
            user = User.objects.get(username=decode.get('username'), email=decode.get('email'))
            if not user:
                raise Exception('user not found')
            user.set_password(request.data.get('new_password'))
            user.save()
            return Response({"message": "Verification Successful", "status": 202, "data": {}},
                            status=status.HTTP_202_ACCEPTED)
        except Exception as ex:
            logger.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)