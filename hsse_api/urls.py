from django.conf.urls import url
from rest_framework.authtoken import views as login_views
from . import views

urlpatterns = [
    url(r'^login/$', login_views.obtain_auth_token),
    url(r'^signin/$', views.User.as_view()),
    url(r'^users/$', views.Users.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view())
]
