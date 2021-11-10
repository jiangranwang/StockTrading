from django.urls import path

from . import views

urlpatterns = [
    path('', views.homepage_view, name='home'),
    path('AdvancedSearch', views.advanced_search, name='AdvancedSearch')
]