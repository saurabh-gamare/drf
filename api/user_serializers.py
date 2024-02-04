# Create a separate app for User Model and add a serializers.py file
# For now we are creating this file naming user_serializers.py

from rest_framework import serializers


class UserPublicSerializer(serializers.Serializer):

    username = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
