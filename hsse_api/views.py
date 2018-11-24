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

    def get_serialized_questions(self, request):
        serialized_questions = None
        if request.query_params.get('formView') == 'userLoginView' or  request.query_params.get('formView') == 'newUserView':
            login_questions = models.Question.objects.filter(form='userLoginView')
            new_user_questions = models.Question.objects.filter(form='newUserView')
            login_serialized = serializers.QuestionSerializer(login_questions, many=True, context={'request', request})
            new_usr_serialized = serializers.QuestionSerializer(new_user_questions, many=True, context={'request', request})
            serialized_questions = { 'userLoginView': login_serialized.data, 'newUserView': new_usr_serialized.data}
        else:
            questions = models.Question.objects.filter(form=request.query_params.get('formView'))
            serialized_questions = serializers.QuestionSerializer(questions, many=True, context={'request', request})
            serialized_questions = serialized_questions.data
        return serialized_questions

    def get(self, request, *args, **kwargs):
        serialized_object = None
        if request.query_params.get('querySection') == 'sites':
            sites = models.Site.objects.all()
            serialized_object = serializers.SiteSerializer(sites, many=True)
            serialized_object = serialized_object.data
        elif request.query_params.get('querySection') == 'questions':
            serialized_object = self.get_serialized_questions(request)

        return Response(serialized_object, status=status.HTTP_200_OK)

class Statistics(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    # serializer_class = serializers.EnvironmentalSerializer

    def get_dashboard_stats(self, request):
        start_date = request.query_params.get('startDate')
        end_date = request.query_params.get('endDate')
        reports = models.Report.objects.all()
        open_reports = len(reports.filter(status="O", created_on__range=(start_date, end_date)))
        in_progress_reports = len(reports.filter(status="IP", created_on__range=(start_date, end_date)))
        closed_reports = len(reports.filter(status="CL", created_on__range=(start_date, end_date)))
        overdue_reports = len(reports.filter(status="OV", created_on__range=(start_date, end_date)))
        # Users
        users = models.User.objects.all()
        users_count = len(users.filter(created_on__range=(start_date, end_date) ))
        contractors = len(users.filter(contractor=True, created_on__range=(start_date, end_date)))
        # Indicators
        indicators = models.EnvironmentalIndicator.objects.all()
        indicators_count = len(indicators.filter(created_on__range=(start_date, end_date)))
        monthly = models.MonthlyReport.objects.all()
        monthly_count = len(monthly.filter(created_on__range=(start_date, end_date)))
        activities = models.SafetyActivity.objects.all()
        activities_count = len(activities.filter(created_on__range=(start_date, end_date)))
        data = {
            "reports": [open_reports, in_progress_reports, closed_reports, overdue_reports],
            "users": [users_count, contractors],
            "indicators": [indicators_count, monthly_count, activities_count],
        }

        return data

    def get(self, request, *args, **kwargs):
        serialized_object = None
        if request.query_params.get('view') == 'dashboard':
            serialized_object = self.get_dashboard_stats(request)

        return Response(serialized_object, status=status.HTTP_200_OK)


class UsersViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()
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
