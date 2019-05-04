from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('destination/<int:number>/', views.showtrip, name="showtrip"),
    path('add/', views.newtrip, name="newtrip"),
    path('createtrip/', views.createtrip, name="createtrip"),
    path('jointrip/<int:number>/', views.jointrip, name="jointrip")
]