from django.urls import path

from . import views

urlpatterns = [
    path('', views.homepage_view, name='home'),
    # path('home', views.home_view, name='home'),
]