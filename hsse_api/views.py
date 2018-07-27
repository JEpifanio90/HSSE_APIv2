from django.http import Http404
from rest_framework import status, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from . import models
from . import serializers

class User(APIView):

    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        """Create new user"""
        user_serializer = serializers.UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user."""

        serializer.save(user_profile=self.request.user)

class UserDetail(APIView):

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk):
        try:
            user_serializer = serializers.UserSerializer(models.User.objects.get(pk=pk))
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        except:
            return Http404

    def put(self, request, pk, format=None):
        user = models.User.objects.get(pk=pk)
        user_serializer = serializers.UserSerializer(user, data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = models.User.objects.get(pk=pk)
        user.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

class Users(APIView):

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        """GET all users"""
        users = models.User.objects.all()
        user_serializer = serializers.UserSerializer(users, many=True)
        
        return Response(user_serializer.data)
