from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^destination/(?P<number>\d+)$', views.showtrip, name="showtrip"),
    url(r'^add$', views.newtrip, name="newtrip"),
    url(r'^createtrip$', views.createtrip, name="createtrip"),
    url(r'^jointrip/(?P<number>\d+)$', views.jointrip, name="jointrip")
]