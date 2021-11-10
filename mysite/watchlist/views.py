from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
#from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Stock, Watchlist,AuthUser
import MySQLdb
from django.forms.models import model_to_dict


  

@login_required(login_url='login')
def watchlist(request):
    res = request.user.username
    user = AuthUser.objects.get(username=res)
    a = user.id
    result = Watchlist.objects.filter(UserId=a)
    arr=[ ]
    for i in result:
        b=i.StockId
        c=model_to_dict(b)
        fresult = Stock.objects.get(stockid=c['stockid'])
        arr.append(fresult)
    return render(request, 'watchlist/watchlist.html',{'watchlist':arr})
    

def watchlist_delete(request):
    res = request.user.username
    user = AuthUser.objects.get(username=res)
    x = user.id
    id = request.GET["id"]
    if Watchlist.objects.filter(UserId=x, StockId=id):
        mystock = Watchlist.objects.filter(UserId=x, StockId=id)
        mystock.delete()
        #mystock.save()
        #return redirect('watchlist')
        return HttpResponse('Stock is successfully removed from your watchlist.')
    else:
        return HttpResponse('Item not found.')



def search_wl(request):
    wlstockid = request.GET.get('wlstockid')
    error_msg = ''
    if not wlstockid:
        error_msg = 'Please input a stock ID'
        print(error_msg)
    try: 
        search_list = Stock.objects.get(stockid = wlstockid)
    except Exception:
        return HttpResponse('Stock not found.')
    #print(model_to_dict(search_list))
    return render(request, 'watchlist/wlresults.html', {'search_list': search_list})
 



def watchlist_add(request):
    res = request.user.username
    user = AuthUser.objects.get(username=res)
    x = user.id
    user2 = AuthUser.objects.get(id=x)
    id = request.GET["id"]   
    stock=Stock.objects.get(stockid = id)
    if Watchlist.objects.filter(StockId=id, UserId=x):
        return HttpResponse("Stock already exists in your watchlist.")
    else: 
        Watchlist.objects.create(StockId=stock, UserId=user2)
        return HttpResponse("Stock is successfully added in your watchlist.")
    