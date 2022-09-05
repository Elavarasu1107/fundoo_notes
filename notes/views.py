from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import NoteSerializer
from .models import Notes
from user.utils import verify_token
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.db import connection
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


class NoteRaw(APIView):
    """
    This class performs CRUD for Notes model using Raw Query
    """

    @verify_token
    def post(self, request):
        """
        This method post data to the database using raw query
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute('insert into notes_notes (title, description, color, user_id) values(%s, %s, %s, %s)',
                               [request.data.get('title'), request.data.get('description'), request.data.get('color'),
                                request.data.get('user')])
                cursor.execute('select * from notes_notes order by id desc limit 1')
                columns = [col[0] for col in cursor.description]
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return Response({"message": "Note Created", "status": 201, "data": data},
                            status=status.HTTP_201_CREATED)
        except Exception as ex:
            logger.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    def get(self, request):
        """
        This method get data from database using raw query
        """
        try:
            notes = Notes.objects.raw('select * from notes_notes where user_id = %s', [request.data.get('user')])
            data = [{"id": x.id, "title": x.title, "description": x.description, "color": x.color, "user": x.user_id}
                    for x in notes]
            return Response({"message": "Data Retrieved", "status": 200, "data": data},
                            status=status.HTTP_200_OK)
        except Exception as ex:
            logger.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    def put(self, request):
        """
        This method update data to the database using raw query
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute('update notes_notes set title = %s, description = %s, color = %s'
                               'where id = %s and user_id = %s',
                               [request.data.get('title'), request.data.get('description'), request.data.get('color'),
                                request.data.get('id'), request.data.get('user')])
                cursor.execute('select * from notes_notes where id = %s', [request.data.get('id')])
                columns = [col[0] for col in cursor.description]
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return Response({"message": "Note Updated", "status": 201, "data": data},
                            status=status.HTTP_201_CREATED)
        except Exception as ex:
            logger.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    def delete(self, request):
        """
        This method delete data from the database using raw query
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute('delete from notes_notes where user_id = %s and id = %s',
                               [request.data.get('user'), request.data.get('id')])
            return Response({"message": "Note Deleted", "status": 204, "data": {}},
                            status=status.HTTP_204_NO_CONTENT)
        except Exception as ex:
            logger.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)
