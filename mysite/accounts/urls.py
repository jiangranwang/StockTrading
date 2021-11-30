from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('home', views.home_view, name='home'),
    path('register', views.register_view, name='register'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('delete_user', views.delete_user, name='delete_user'),
    path('update_password', views.update_password, name='update_password'),
    path('delete/', views.delete)
]