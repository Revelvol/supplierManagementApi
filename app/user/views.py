from django.shortcuts import render
from base.models import User
from .serializers import UserSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
