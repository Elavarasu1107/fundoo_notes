from django.shortcuts import render
from django.contrib.auth import authenticate
from .models import User
from .serializers import RegisterSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
import logging
from rest_framework import status

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
            user = authenticate(**request.data)
            if not user:
                raise Exception("Invalid Credentials")
            return Response({"message": "Login Successful", "status": 202, "data": {}},
                            status=status.HTTP_202_ACCEPTED)
        except Exception as ex:
            logger.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)
