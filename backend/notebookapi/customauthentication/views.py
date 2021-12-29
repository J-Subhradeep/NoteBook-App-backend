from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Note
from .serializers import UserSerializer
import datetime
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

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            User.objects.create_user(**data)
            return Response(serializer.data)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
# class LoginUserApi(APIView):
#     def post(self, request, *args, **kwargs):
#         data=request.data
#         email = data.get('email')
#         password = data.get('password')
