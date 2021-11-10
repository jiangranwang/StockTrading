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

# # Create your views here.
# @login_required(login_url='login')
# def home_view(request):
#     watchlist = Stock.objects.raw('select * from Stock where stockid in '
#                                   '(select stockid from Watchlist where UserId = '
#                                   '(select id from auth_user where username = %s))', [request.user.username])
#     cursor = connection.cursor()
#     cursor.execute('select stockname, freq from Stock natural join '
#                    '(select count(userid) as freq, stockid from Watchlist '
#                    'group by stockid having stockid in '
#                    '(select stockid from Watchlist where UserId = '
#                    '(select id from auth_user where username = %s))) a '
#                    'order by freq desc, stockname asc', [request.user.username])
#     rows = cursor.fetchall()
#     freqs = []
#     for r in rows:
#         freqs.append({'stockname': r[0], 'freq': r[1]})
#     return render(request, 'accounts/home.html', {'watchlist': watchlist, 'freqs': freqs})


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

