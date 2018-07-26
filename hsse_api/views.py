from django.http import Http404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models
from . import serializers


# Create your views here.

class Users(APIView):

    # permission_classes = (permissions.IsAuthenticatedOrReadOnly)

    def get(self, request, format=None):
        """GET all users"""
        users = models.User.objects.all()
        user_serializer = serializers.UserSerializer(users, many=True)

        return Response(user_serializer.data)

    def post(self, request, format=None):
        """Create new user"""
        user_serializer = serializers.UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):

    # permission_classes = (permissions.IsAuthenticatedOrReadOnly)

    def get_object(self, pk):
        try:
            return models.User.objects.get(pk=pk)
        except:
            return Http404

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        user_serializer = serializers.UserSerializer(user, data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
