from django.http import Http404
from rest_framework import status, permissions, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from hsse_api import models
from hsse_api import serializers

class Login(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        credentials = Token.objects.get_or_create(user=user)
        serialized_user = serializers.User_Serializer(user).data
        serialized_user['token'] = credentials[0].key
        return Response(serialized_user, status=status.HTTP_200_OK)

class Users_View_set(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.User_Serializer
    queryset = models.User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_user_token(self, request):
        new_user_data = {
            "username": request.data['email'],
            "password": request.data['password']
        }
        serializer = AuthTokenSerializer(data=new_user_data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        credentials = Token.objects.get_or_create(user=user)
        return credentials[0].key

    def create(self, request, *args, **kwargs):
        """Create new user"""
        serialized_user = self.serializer_class(data=request.data)
        serialized_user.is_valid(raise_exception=True)
        if serialized_user.is_valid():
            serialized_user.save()
            new_user = serialized_user.data
            new_user['token'] = self.get_user_token(request)
            return Response(new_user, status=status.HTTP_201_CREATED)
        return Response(serialized_user.errors, status=status.HTTP_400_BAD_REQUEST)

class Audits_View_Set(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.Audit_Serializer
    queryset = models.Audit_Inspection.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

class Corrective_View_Set(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.Corrective_Serializer
    queryset = models.Corrective_Action.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

class Communities_View_Set(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.Community_Serializer
    queryset = models.Employee_Community_Activity.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

class Environmental_Indicators_View_Set(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.Environmental_Serializer
    queryset = models.Environmental_Indicators.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

class Reports_View_Set(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.Report_Serializer
    queryset = models.Report.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

class Monthly_Reports_View_Set(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.Montly_Report_Serializer
    queryset = models.Monthly_Reports.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

class Safety_Activities_View_Set(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.Safety_Activity_Serializer
    queryset = models.Safety_Activity.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

class Sites_View_Set(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.Site_Serializer
    queryset = models.Site.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
