from django.shortcuts import render
from django.db import connection

from .models import Stock   


def homepage_view(request):
    print("request method = " , request.method)
    if request.method == 'POST':
            keyword = request.POST['keyword']
            keyword = '%' + keyword + '%'
            queryset = Stock.objects.raw('SELECT * FROM Stock WHERE stockname like %s', [keyword])
            # print(queryset)
            # for q in queryset:
            #     print("stock name %s price %i" %(q.stockname, q.price))
            context = {'queryset': queryset}
            return render(request, 'homepage/homePage.html', context)
    queryset = []
    context = {'queryset': queryset}
    return render(request, 'homepage/homePage.html', context)

def advanced_search(request):
    if request.method == 'POST':
            stockname = request.POST['stockname']
            stockname = '%' + stockname + '%'
            company = request.POST['company']
            company = '%' + company + '%'
            price = request.POST['price']
            price = int(price)
            cursor = connection.cursor()
            cursor.execute('''
                            select stockname, company, price, freq
				            from Stock natural join (
                                select count(userid) as freq, stockid 
                                from Watchlist 
                                group by stockid) w
                            WHERE stockname like %s and company like %s and price >= %s
                            order by freq desc, stockname asc
                            ''', [stockname,company,price])
            rows = cursor.fetchall()
            queryset = []
            for r in rows:
                queryset.append({'stockname': r[0], 'company': r[1], 'price': r[2]})

            context = {'queryset': queryset}
            return render(request, 'homepage/advancedSearch.html', context)

    # queryset = Stock.objects.all()
    queryset = []
    context = {'queryset': queryset}
    return render(request, 'homepage/advancedSearch.html', context)

