from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^users/$', views.users)
    # url(r'^snippets/(?P<pk>[0-9]+)/$', views.snippet_detail),
]
