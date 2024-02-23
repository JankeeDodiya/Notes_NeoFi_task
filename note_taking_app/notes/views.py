from django.shortcuts import render

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import *
from .serializers import *


# Login view
@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def note_create(request):

    request.data['owner'] = request.user.id

    serializer = NoteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def note_detail(request, pk):
    try:
        note = Note.objects.get(pk=pk, owner=request.user)
    except Note.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = NoteSerializer(note)
    return Response(serializer.data)


# Share note view
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def share_note(request):
    note_id = request.data.get('note_id')
    shared_with = request.data.get('shared_with')
    try:
        note = Note.objects.get(pk=note_id, owner=request.user)
        for username in shared_with:
            user = User.objects.get(username=username)
            note.shared_with.add(user)
        note.save()
        return Response({'message': 'Note shared successfully'}, status=status.HTTP_200_OK)
    except Note.DoesNotExist:
        return Response({'error': 'Note not found'}, status=status.HTTP_404_NOT_FOUND)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


# Update note view
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_note(request, pk):
    try:
        note = Note.objects.get(pk=pk, owner=request.user)
        serializer = NoteSerializer(note, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Note.DoesNotExist:
        return Response({'error': 'Note not found'}, status=status.HTTP_404_NOT_FOUND)


# Get version history view
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def version_history(request, pk):
    try:
        note = Note.objects.get(pk=pk, owner=request.user)
        versions = note.version_set.all()  # Assuming Version is a related model
        # Serialize versions if needed
        return Response({'versions': versions}, status=status.HTTP_200_OK)
    except Note.DoesNotExist:
        return Response({'error': 'Note not found'}, status=status.HTTP_404_NOT_FOUND)
