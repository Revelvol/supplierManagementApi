from .serializers import (UserSerializer,
                          AuthTokenSerializer)
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework import authentication, permissions


class CreateUserView(generics.CreateAPIView, generics.ListAPIView):
    """Create new user"""
    serializer_class = UserSerializer

    def get_queryset(self):
        return get_user_model().objects.all()

class ManageUserView(generics.RetrieveUpdateAPIView):
    """edit the authenticated user by token"""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class CreateTokenView(generics.CreateAPIView):
    """create token for registered user"""
    serializer_class = AuthTokenSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data.get('user')
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)



