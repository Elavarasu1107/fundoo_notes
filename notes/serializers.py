from rest_framework import serializers
from .models import Notes
from drf_yasg import openapi


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['id', 'title', 'description', 'color', 'user']
        swagger_schema_fields = {"required": ['title', 'description', 'color'], "type": openapi.TYPE_OBJECT,
                                 "properties": {
                                     "title": openapi.Schema(
                                         title="title",
                                         type=openapi.TYPE_STRING,
                                     ),
                                     "description": openapi.Schema(
                                         title="description",
                                         type=openapi.TYPE_STRING,
                                     ),
                                     "color": openapi.Schema(
                                         title="color",
                                         type=openapi.TYPE_STRING,
                                     )
                                 }}
