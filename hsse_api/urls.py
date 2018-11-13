from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from hsse_api import views

router = DefaultRouter()
router.register(r'environmental/indicators', views.EnvironmentalindicatorsViewSet)
router.register(r'monthly/reports', views.MonthlyReportsViewSet)
router.register(r'reports', views.ReportsViewSet)
router.register(r'safety/activities', views.SafetyActivitiesViewSet)
router.register(r'sites', views.SitesViewSet)
router.register(r'users', views.UsersViewSet)
router.register(r'questions', views.QuestionsViewSet)

urlpatterns = [
    url(r'^login/?$', views.Login.as_view()),
    url(r'^signin/?$', views.SignIn.as_view()),
    url(r'^public/sites?$', views.Public.as_view()),
    url(r'^dashboard/?$', views.Dashboard.as_view()),
    url(r'^', include(router.urls))
]
