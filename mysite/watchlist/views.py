from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Stock, Watchlist, AuthUser
from django.db import connection
cursor = connection.cursor()


@login_required(login_url='login')
def index(request):
    username = request.user.username
    user = AuthUser.objects.raw('select * from auth_user where username = %s', [username])[0]
    result = Watchlist.objects.raw('select * from Watchlist where userid = %s', [user.id])
    arr = []
    for i in result:
        res = Stock.objects.raw('select * from Stock where stockid = %s', [i.StockId.stockid])[0]
        arr.append(res)
    return render(request, 'watchlist/watchlist.html', {'watchlist': arr})


def add(request):
    username = request.user.username
    user = AuthUser.objects.raw('select * from auth_user where username = %s', [username])[0]
    stockId = request.GET["id"]
    if len(Watchlist.objects.raw('select * from Watchlist where stockid = %s and userid = %s', [stockId, user.id])) > 0:
        messages.error(request, "Stock already exists in your watchlist.")
    else:
        cursor.execute('insert into Watchlist (userid, stockid) values (%s, %s)', [user.id, stockId])
        messages.success(request, "Stock is successfully added in your watchlist.")
    return redirect('index')


def delete(request):
    username = request.user.username
    user = AuthUser.objects.raw('select * from auth_user where username = %s', [username])[0]
    stockId = request.GET["id"]
    if Watchlist.objects.raw('select * from Watchlist where userid = %s and stockid = %s', [user.id, stockId]):
        cursor.execute('delete from Watchlist where userid = %s and stockid = %s', [user.id, stockId])
        messages.success(request, 'Stock is successfully removed from your watchlist.')
    else:
        messages.error(request, 'Item not found.')
    return redirect('index')


def search(request):
    stockId = request.GET.get('wlstockid')
    if not stockId:
        messages.error(request, 'Please input a stock id')
        return redirect('index')
    else:
        result = Stock.objects.raw('select * from Stock where stockid = %s', [stockId])
        if len(result) == 0:
            messages.error(request, 'Stock id invalid')
            return redirect('index')
        return render(request, 'watchlist/wlresults.html', {'search_list': result[0]})
