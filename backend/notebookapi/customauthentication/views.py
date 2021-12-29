from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Note
from .serializers import UserSerializer
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
            # print(data.get('token'))
            # payload = jwt.decode(data.get('token'), settings.SECRET_KEY)
            # print(payload)
            user = User.objects.filter(email=data.get(
                'email'))
            serializer = UserSerializer(user, many=True)
            # if serializer.is_valid():
            # return Response(serializer.data)
            if serializer.data:
                return Response(serializer.data)
            return Response({"error": True}, status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError as error:
            return Response({'error': 'error'})
        # email = data.get('email')
        # password = data.get('password')
