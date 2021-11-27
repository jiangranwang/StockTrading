from django.db.models.query import QuerySet
from django.shortcuts import render
from django.db import connection

# Create your views here.

from django.views import View
from .models import Stock

class Index(View):
    template = 'stock/index.html'

    def get(self, request):
        return render(request, self.template)
    


def stock_graph(request, StockName):
    #stock = Stock.objects.get(stockname=StockName)
    cursor = connection.cursor()
    cursor.execute('SELECT s.Time, k.Price, k.High, k.Low, s.Price FROM StockPrice s join Stock k using(stockid) where k.stockname = %s',[StockName])
    #queryset = Stock.objects.raw('SELECT s.Time, k.Price, k.High, k.Low, s.Price FROM StockPrice s join Stock k using(stockid) where k.stockname = StockName')
    rows = cursor.fetchall()
    stockinfo = []
    for r in rows:
        stockinfo.append({'time': r[0], 'open': r[4], 'high': r[2], 'low': r[3], 'close': r[2]})

    context = {'stockinfo': stockinfo}
    #for q in queryset:
    return render(request, 'stock/stock-graph.html', context)
    

def layout_sidenav_light(request):
    print(request.method)
    
    return render(request, 'stock/layout-sidenav-light.html')

def layout_static(request):
    print(request.method)
    
    return render(request, 'stock/layout-static.html')

def test(request):
    print(request.method)
    
    return render(request, 'stock/test.html')
