from rest_framework import serializers
from .models import Note, Version
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user



class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields =  '__all__'

class SharedNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'title', 'content']

class VersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = '__all__'
