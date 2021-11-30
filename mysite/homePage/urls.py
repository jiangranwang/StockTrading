from django.urls import path

from . import views

urlpatterns = [
    path('', views.homepage_view, name='homepage'),
    path('AdvancedSearch', views.advanced_search, name='AdvancedSearch'),
    path('add/', views.add)
]