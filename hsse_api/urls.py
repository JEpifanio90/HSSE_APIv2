from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from hsse_api import views

router = DefaultRouter()
router.register(r'audits', views.Audits_View_Set)
router.register(r'community/activities', views.Communities_View_Set)
router.register(r'corrective/actions', views.Corrective_View_Set)
router.register(r'environmental/indicators', views.Environmental_Indicators_View_Set)
router.register(r'monthly/reports', views.Monthly_Reports_View_Set)
router.register(r'reports', views.Reports_View_Set)
router.register(r'safety/activities', views.Safety_Activities_View_Set)
router.register(r'sites', views.Sites_View_Set)
router.register(r'users', views.Users_View_set)

urlpatterns = [
    url(r'^login/?$', views.Login.as_view()),
    url(r'^signin/?$', views.Sign_In.as_view()),
    url(r'^public/sites?$', views.Public.as_view()),
    url(r'^', include(router.urls))
]
