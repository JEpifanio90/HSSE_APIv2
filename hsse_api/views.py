from django.http import Http404
from django.db.models import Sum
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
        questions = models.Question.objects.all()
        if request.query_params.get('formView') in ['userLoginView', 'newUserView']:
            login_questions = questions.filter(form='userLoginView')
            new_user_questions = questions.filter(form='newUserView')
            login_serialized = serializers.QuestionSerializer(login_questions, many=True, context={'request', request})
            new_usr_serialized = serializers.QuestionSerializer(new_user_questions, many=True, context={'request', request})
            serialized_questions = { 'userLoginView': login_serialized.data, 'newUserView': new_usr_serialized.data}
        elif request.query_params.get('formView') in ['personalInfoView', 'incidentDescriptionView', 'eventDescriptionView', 'incidentAnalysisView', 'approvalsView']:
            personal_questions = questions.filter(form='personalInfoView')
            description_questions = questions.filter(form='incidentDescriptionView')
            event_questions = questions.filter(form='eventDescriptionView')
            incident_questions = questions.filter(form='incidentAnalysisView')
            approval_questions = questions.filter(form='approvalsView')
            personal_serialized = serializers.QuestionSerializer(personal_questions, many=True, context={'request', request})
            description_serialized = serializers.QuestionSerializer(description_questions, many=True, context={'request', request})
            event_serialized = serializers.QuestionSerializer(event_questions, many=True, context={'request', request})
            incident_serialized = serializers.QuestionSerializer(incident_questions, many=True, context={'request', request})
            approval_serialized = serializers.QuestionSerializer(approval_questions, many=True, context={'request', request})
            serialized_questions = {
                'personalInfoQs': personal_serialized.data,
                'incidentDescriptionQs': description_serialized.data,
                'eventDescriptionQs': event_serialized.data,
                'incidentAnalysisQs': incident_serialized.data,
                'approvalsQs': approval_serialized.data
            }
        else:
            questions = questions.filter(form=request.query_params.get('formView'))
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
        users_count = len(users.filter(contractor=False, created_on__range=(start_date, end_date) ))
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
    
    def get_environmental_indicators_stats(self, request):
        data = dict()
        indicators = models.EnvironmentalIndicator.objects.filter(created_on__range=(request.query_params.get('startDate'), request.query_params.get('endDate')))
        data['totalRenewableElectricityConsumed'] = indicators.aggregate(Sum('renewable_electricity_consumed'))['renewable_electricity_consumed__sum']
        data['totalElectricityConsumed'] = indicators.aggregate(Sum('non_renewable_electricity_consumed'))['non_renewable_electricity_consumed__sum']
        data['totalConsumedGas'] = indicators.aggregate(Sum('consumed_gas'))['consumed_gas__sum']
        data['totalConsumedWater'] = indicators.aggregate(Sum('consumed_water'))['consumed_water__sum']
        data['totalDangerousWasteGenerated'] = indicators.aggregate(Sum('dangerous_waste_generated'))['dangerous_waste_generated__sum']
        data['totalNonDangerousWasteGenerated'] = indicators.aggregate(Sum('non_dangerous_waste_generated'))['non_dangerous_waste_generated__sum']
        data['totalWasteSold'] = indicators.aggregate(Sum('waste_sold'))['waste_sold__sum']
        data['totalToLandfield'] = indicators.aggregate(Sum('waste_to_landfield'))['waste_to_landfield__sum']
        data['totalWasteRecycled'] = indicators.aggregate(Sum('waste_recycled'))['waste_recycled__sum']

        return data
    
    def get_monthly_reports_stats(self, request):
        data = dict()
        indicators = models.MonthlyReport.objects.filter(created_on__range=(request.query_params.get('startDate'), request.query_params.get('endDate')))
        data['totalEmployees'] = indicators.aggregate(Sum('no_employees'))['no_employees__sum']
        data['totalContractors'] = indicators.aggregate(Sum('no_contractors'))['no_contractors__sum']
        data['totalWorkedEmployeehours'] = indicators.aggregate(Sum('worked_employee_hours'))['worked_employee_hours__sum']
        data['totalWorkedContractorHours'] = indicators.aggregate(Sum('worked_contractor_hours'))['worked_contractor_hours__sum']
        data['totalReportsOverdue'] = indicators.aggregate(Sum('no_reports_overdue'))['no_reports_overdue__sum']
        data['totalReportsClosed'] = indicators.aggregate(Sum('no_reports_closed'))['no_reports_closed__sum']
        data['totalReportsIP'] = indicators.aggregate(Sum('no_reports_in_progress'))['no_reports_in_progress__sum']
        data['totalReportsOpen'] = indicators.aggregate(Sum('no_reports_open'))['no_reports_open__sum']

        return data

    def get(self, request, *args, **kwargs):
        serialized_object = None
        if request.query_params.get('view') == 'dashboardView':
            serialized_object = self.get_dashboard_stats(request)
        elif  request.query_params.get('view') == 'environmentalIndicatorsView':
            serialized_object = self.get_environmental_indicators_stats(request)
        elif request.query_params.get('view') == 'monthlyReportsView':
            serialized_object = self.get_monthly_reports_stats(request)

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
