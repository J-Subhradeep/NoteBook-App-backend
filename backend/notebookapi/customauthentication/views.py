from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Note
from .serializers import UserSerializer, NotesSerializer
import datetime
import jwt
from django.conf import settings
# Create your views here.


class UserView(APIView):
    def get(self, request, *args, **kwargs):

        print(request.data)
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        if request.data.get('id'):
            queryset = User.objects.get(pk=request.data['id'])
            serializer = UserSerializer(queryset)
        return Response(serializer.data)

    def post(self, request, pk=None, *args, **kwargs):
        data = request.data
        if data.get('id'):
            user = User.objects.get(pk=data.get('id'))
            serializer = UserSerializer(user)

            return Response(serializer.data)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            User.objects.create_user(**data)
            return Response(serializer.data)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class LoginUserApi(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            user = User.objects.filter(email=data.get(
                'email'))
            serializer = UserSerializer(user, many=True)
            if serializer.data:
                return Response(serializer.data)
            return Response({"error": True}, status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError as error:
            return Response({'error': 'error'})


class VarifyUser(APIView):
    def post(self, request, *args, **kwargs):
        token = request.data.get('token')
        try:
            payload = jwt.decode(token, str(settings.SECRET_KEY), ['HS256'])
            user = User.objects.get(pk=payload.get('user_id'))
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except:
            print("error")
            return Response({'error': True})


class UsersNotes(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        print(data)
        token = request.data.get('token')
        try:
            payload = jwt.decode(token, str(settings.SECRET_KEY), ['HS256'])
            id = payload.get('user_id')

            user = User.objects.get(pk=id)
            notes = user.note_set.all()
            serializer = NotesSerializer(notes, many=True)
            return Response(serializer.data)
        except:
            return Response({'error': True})


class NotesPost(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        
        return Response({})
