#from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('watchlist/', views.watchlist),
    path('watchlist_delete/',views.watchlist_delete),
    #url(r'watchlist_delete/',views.watchlist_delete),
    path('watchlist_add/',views.watchlist_add),
    path('search_wl/',views.search_wl)
]