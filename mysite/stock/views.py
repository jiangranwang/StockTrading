from django.shortcuts import render

# Create your views here.

from django.views import View
from .models import Stock

class Index(View):
    template = 'stock/index.html'

    def get(self, request):
        return render(request, self.template)
    


def stock_graph(request, StockName):
    stock = Stock.objects.get(stockname=StockName)
    return render(request, 'stock/stock-graph.html',{'StockName': stock})
    

def layout_sidenav_light(request):
    print(request.method)
    
    return render(request, 'stock/layout-sidenav-light.html')

def layout_static(request):
    print(request.method)
    
    return render(request, 'stock/layout-static.html')
