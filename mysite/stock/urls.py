from django.urls import path

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('index', views.Index.as_view(), name='index'),
    path('layout-static', views.layout_static, name='layout-static'),
    path('layout-sidenav-light', views.layout_sidenav_light, name='layout-sidenav-light'),
    path('<StockName>', views.stock_graph, name='stock-graph'),

]


