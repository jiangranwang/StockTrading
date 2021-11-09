from django.shortcuts import render
from .models import Stock   


def homepage_view(request):
    print("request method = " , request.method)
    if request.method == 'POST':
            keyword = request.POST['keyword']
            keyword = '%' + keyword + '%'
            queryset = Stock.objects.raw('SELECT * FROM Stock WHERE stockname like %s', [keyword])
            print(queryset)
            for q in queryset:
                print("stock name %s price %i" %(q.stockname, q.price))
            context = {'queryset': queryset}
            return render(request, 'homepage/homePage.html', context)
    queryset = Stock.objects.all()
    context = {'queryset': queryset}
    return render(request, 'homepage/homePage.html', context)

