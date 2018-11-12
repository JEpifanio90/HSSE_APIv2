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
        serialized_user = serializers.UserSerializer(user).data
        serialized_user['token'] = credentials[0].key
        return Response(serialized_user, status=status.HTTP_200_OK)

class SignIn(APIView):

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

    def post(self, request, *args, **kwargs):
        """Create new user"""
        serialized_user = serializers.UserSerializer(data=request.data, context={'request': request})
        if serialized_user.is_valid(raise_exception=True):
            serialized_user.save()
            new_user = serialized_user.data
            new_user['token'] = self.get_user_token(request)
            return Response(new_user, status=status.HTTP_201_CREATED)
        return Response(serialized_user.errors, status=status.HTTP_400_BAD_REQUEST)

class Public(APIView):

    def get(self, request, *args, **kwargs):
        sites = models.Site.objects.all()
        serialized_sites = serializers.SiteSerializer(sites, many=True)

        return Response(serialized_sites.data, status=status.HTTP_200_OK)

# ! This sucks biiiiig time. RE-DO
class Dashboard(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.EnvironmentalSerializer

    def post(self, request, *args, **kwargs):
        dates = serializers.Date_Serializer(data=request.data, context={'request': request})
        if dates.is_valid():
            # Reports
            reports = models.Report.objects.all();
            open_reports = len(reports.filter(status="O", created_on=dates.data['start_date'])) + len(reports.filter(status="O", created_on=dates.data['end_date']))
            in_progress_reports = len(reports.filter(status="IP", created_on=dates.data['start_date'])) + len(reports.filter(status="IP", created_on=dates.data['end_date']))
            closed_reports = len(reports.filter(status="CL", created_on=dates.data['start_date'])) + len(reports.filter(status="CL", created_on=dates.data['end_date']))
            overdue_reports = len(reports.filter(status="OV", created_on=dates.data['start_date'])) + len(reports.filter(status="OV", created_on=dates.data['end_date']))
            # Users
            users = models.User.objects.all()
            users_count = len(users.filter(created_on=dates.data['start_date'])) + len(users.filter(created_on=dates.data['end_date']))
            contractors = len(users.filter(contractor=True, created_on=dates.data['start_date'])) + len(users.filter(contractor=True, created_on=dates.data['end_date']))
            # Indicators
            indicators = models.EnvironmentalIndicator.objects.all()
            indicators_count = len(indicators.filter(created_on=dates.data['start_date'])) + len(indicators.filter(created_on=dates.data['end_date']))
            monthly = models.MonthlyReport.objects.all()
            monthly_count = len(monthly.filter(created_on=dates.data['start_date'])) + len(monthly.filter(created_on=dates.data['end_date']))
            activities = models.SafetyActivity.objects.all()
            activities_count = len(activities.filter(created_on=dates.data['start_date'])) + len(activities.filter(created_on=dates.data['end_date']))

            data = {
                "reports": [open_reports, in_progress_reports, closed_reports, overdue_reports],
                "users": [users_count, contractors],
                "indicators": [indicators_count, monthly_count, activities_count],
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(dates.errors, status=status.HTTP_400_BAD_REQUEST)

class UsersViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

class AuditsViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.AuditSerializer
    queryset = models.AuditInspection.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

class CommunitiesViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.CommunitySerializer
    queryset = models.EmployeeCommunityActivity.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

class EnvironmentalindicatorsViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.EnvironmentalSerializer
    queryset = models.EnvironmentalIndicator.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

class ReportsViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ReportSerializer
    queryset = models.Report.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

class MonthlyReportsViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.MonthlyReportSerializer
    queryset = models.MonthlyReport.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

class SafetyActivitiesViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.SafetyActivitySerializer
    queryset = models.SafetyActivity.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

class SitesViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.SiteSerializer
    queryset = models.Site.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

class QuestionsViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.Question_Serializer
    queryset = models.Question.objects.all()
