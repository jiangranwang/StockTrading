from django.shortcuts import render
from .models import Stock   


def homepage_view(request):
    if request.method == 'POST':
        if request.POST['submit'] == 'searchKeyword':
                keyword = request.POST['keyword']
                queryset = Stock.objects.get(stockname__contains = keyword)
                context = {'queryset': queryset}
                return render(request, 'homepage/homePage.html', context)

