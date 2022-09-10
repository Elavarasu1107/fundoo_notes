from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import NoteSerializer
from .models import Notes
from user.utils import verify_token, JWT
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets
import logging

logging.basicConfig(filename='fundoo_note.log', encoding='utf-8', level=logging.DEBUG,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger()


class Note(APIView):
    """
    This class performs CRUD for Notes model
    """

    @swagger_auto_schema(request_body=NoteSerializer, operation_summary='Post Notes')
    @verify_token
    def post(self, request):
        """
        This method create note for user
        """
        try:
            serializer = NoteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Note Created", "status": 201, "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as ex:
            logger.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary='Get Notes')
    @verify_token
    def get(self, request):
        """
        This method retrieves notes of a user
        """
        try:
            notes = Notes.objects.filter(user_id=request.data.get('user'))
            serializer = NoteSerializer(notes, many=True)
            return Response({"message": "Data Retrieved", "status": 200, "data": serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as ex:
            logger.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=openapi.Schema(type=openapi.TYPE_OBJECT,
                                                     properties={'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                                                 'title': openapi.Schema(type=openapi.TYPE_STRING),
                                                                 'description': openapi.Schema(
                                                                     type=openapi.TYPE_STRING),
                                                                 'color': openapi.Schema(type=openapi.TYPE_STRING)},
                                                     required=['id', 'title', 'description', 'color']),
                         operation_summary='Update Notes')
    @verify_token
    def put(self, request):
        """
        This method update the note of a user
        """
        try:
            note_object = Notes.objects.get(id=request.data.get('id'), user=request.data.get('user'))
            serializer = NoteSerializer(note_object, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Note Updated", "status": 201, "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as ex:
            logger.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=openapi.Schema(type=openapi.TYPE_OBJECT,
                                                     properties={'id': openapi.Schema(type=openapi.TYPE_INTEGER)},
                                                     required=['id']),
                         operation_summary='Delete Notes')
    @verify_token
    def delete(self, request):
        """
        This method delete the note of a user
        """
        try:
            note_object = Notes.objects.get(id=request.data.get('id'), user=request.data.get('user'))
            note_object.delete()
            return Response({"message": "Note Deleted", "status": 204, "data": {}},
                            status=status.HTTP_204_NO_CONTENT)
        except Exception as ex:
            logger.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)


class NoteMixins(mixins.CreateModelMixin,
                 mixins.ListModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 generics.GenericAPIView):
    serializer_class = NoteSerializer

    def get_queryset(self):
        return Notes.objects.filter(user_id=self.request.data.get('user'))

    @verify_token
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @verify_token
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @verify_token
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @verify_token
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class NoteViewSet(viewsets.ViewSet):

    @verify_token
    def list(self, request):
        try:
            notes = Notes.objects.filter(user_id=request.data.get('user'))
            serializer = NoteSerializer(notes, many=True)
            return Response({"message": "Data Retrieved", "status": 200, "data": serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as ex:
            logger.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    def create(self, request):
        try:
            serializer = NoteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Note Created", "status": 201, "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as ex:
            logger.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    def update(self, request):
        try:
            note_object = Notes.objects.get(id=request.data.get('id'), user=request.data.get('user'))
            serializer = NoteSerializer(note_object, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Note Updated", "status": 201, "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as ex:
            logger.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    def destroy(self, request):
        try:
            note_object = Notes.objects.get(id=request.data.get('id'), user=request.data.get('user'))
            note_object.delete()
            return Response({"message": "Note Deleted", "status": 204, "data": {}},
                            status=status.HTTP_204_NO_CONTENT)
        except Exception as ex:
            logger.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)
