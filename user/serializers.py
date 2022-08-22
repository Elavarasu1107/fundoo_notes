from rest_framework import serializers
from .models import User
import logging

logging.basicConfig(filename='fundoo_note.log', encoding='utf-8', level=logging.DEBUG,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger()


class RegisterSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        """
        Create and return a new user instance, given the validated data.
        """
        try:
            return User.objects.create_user(**validated_data)
        except Exception as ex:
            logger.exception(ex)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'phone', 'location', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}
