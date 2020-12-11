from rest_framework import serializers
from documents.models import Document
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('name', 'path', 'owner', 'is_public', 'is_important')
        read_only_fields = ['owner']
