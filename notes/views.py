from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import NoteSerializer, CollaboratorSerializer
from .models import Notes
from user.utils import verify_token
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from user.models import User
from django.db.models import Q
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
            lookup = Q(collaborator__id=request.data.get('user')) | Q(user__id=request.data.get('user'))
            collaborator_notes = Notes.objects.filter(lookup)
            serializer = NoteSerializer(collaborator_notes, many=True)
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


class NoteCollaborator(APIView):

    @swagger_auto_schema(request_body=openapi.Schema(type=openapi.TYPE_OBJECT,
                                                     properties={'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                                                 'collaborator': openapi.Schema(type=openapi.TYPE_ARRAY,
                                                                                                items=openapi.Items(type=openapi.TYPE_INTEGER))},
                                                     required=['id', 'collaborator']),
                         operation_summary='Post Collaborator')
    @verify_token
    def post(self, request):
        try:
            note = Notes.objects.get(id=request.data.get('id'))
            serializer = CollaboratorSerializer(note, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Collaborator Added", "status": 201, "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as ex:
            logger.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=openapi.Schema(type=openapi.TYPE_OBJECT,
                                                     properties={'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                                                 'collaborator': openapi.Schema(type=openapi.TYPE_ARRAY,
                                                                                                items=openapi.Items(type=openapi.TYPE_INTEGER))},
                                                     required=['id', 'collaborator']),
                         operation_summary='Post Collaborator')
    @verify_token
    def delete(self, request):
        try:
            note = Notes.objects.get(id=request.data.get('id'))
            note.collaborator.remove(*request.data.get('collaborator'))
            return Response({"message": "Collaborator Removed", "status": 204, "data": {}},
                            status=status.HTTP_204_NO_CONTENT)
        except Exception as ex:
            logger.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)
