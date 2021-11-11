from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('watchlist/', views.index),
    path('delete/', views.delete),
    path('add/', views.add),
    path('search/', views.search)
]