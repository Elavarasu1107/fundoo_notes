from rest_framework import serializers
from .models import Notes, Labels
from drf_yasg import openapi


class Label(serializers.ModelSerializer):
    class Meta:
        model = Labels
        fields = ['id']


class NoteSerializer(serializers.ModelSerializer):
    label = Label(many=True, read_only=True)

    class Meta:
        model = Notes
        fields = ['id', 'title', 'description', 'color', 'user', 'collaborator', 'label']
        ref_name = 'NoteSerializer'
        read_only_fields = ['collaborator', 'label']
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


class CollaboratorSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        instance.collaborator.add(*validated_data.get('collaborator'))
        instance.save()
        return instance

    class Meta:
        model = Notes
        fields = ['id', 'collaborator']


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Labels
        fields = ['id', 'title', 'color', 'font', 'user']
        ref_name = 'LabelSerializer'
        swagger_schema_fields = {"required": ['title', 'color', 'font'], "type": openapi.TYPE_OBJECT,
                                 "properties": {
                                     "title": openapi.Schema(
                                         title="title",
                                         type=openapi.TYPE_STRING,
                                     ),
                                     "color": openapi.Schema(
                                         title="color",
                                         type=openapi.TYPE_STRING,
                                     ),
                                     "font": openapi.Schema(
                                         title="font",
                                         type=openapi.TYPE_STRING,
                                     )
                                 }}


class LabelNoteSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        instance.label.add(*validated_data.get('label'))
        instance.save()
        return instance

    class Meta:
        model = Notes
        fields = ['id', 'label']
