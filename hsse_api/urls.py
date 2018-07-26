from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^users/$', views.Users.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view())
]
