from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Stock, AuthUser, Watchlist
from django.db import connection

cursor = connection.cursor()


def homepage_view(request):
    print("request method = ", request.method)
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
        if price == '':
            price = 0
        else:
            price = int(price)
        cursor = connection.cursor()
        cursor.execute('''
                            select stockname, company, price, freq, stockid
				            from Stock natural join (
                                select count(userid) as freq, stockid 
                                from Watchlist 
                                group by stockid) w
                            WHERE stockname like %s and company like %s and price >= %s
                            order by freq desc, stockname asc
                            ''', [stockname, company, price])
        rows = cursor.fetchall()
        queryset = []
        for r in rows:
            queryset.append({'stockname': r[0], 'company': r[1], 'price': r[2], 'stockid': r[4]})

        context = {'queryset': queryset, 'result': True}
        return render(request, 'homepage/advancedSearch.html', context)

    # queryset = Stock.objects.all()
    queryset = []
    context = {'queryset': queryset}
    return render(request, 'homepage/advancedSearch.html', context)


def add(request):
    username = request.user.username
    user = AuthUser.objects.raw('select * from auth_user where username = %s', [username])[0]
    stockId = request.GET["id"]
    stockName = request.GET["name"]
    if len(Watchlist.objects.raw('select * from Watchlist where stockid = %s and userid = %s', [stockId, user.id])) > 0:
        messages.error(request, "Stock " + stockName + " already exists in your watchlist.")
    else:
        cursor.execute('insert into Watchlist (userid, stockid) values (%s, %s)', [user.id, stockId])
        messages.success(request, "Stock " + stockName + " is successfully added in your watchlist.")
    return redirect('homepage')
