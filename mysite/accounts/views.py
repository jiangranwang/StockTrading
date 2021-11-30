from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.db import connection
from .forms import CreateUserForm
from .models import Stock
cursor = connection.cursor()


@login_required(login_url='login')
def home_view(request):
    print(request.method)
    watchlist = Stock.objects.raw('select * from Stock where stockid in '
                                  '(select stockid from Watchlist where UserId = '
                                  '(select id from auth_user where username = %s))', [request.user.username])
    cursor.execute('select stockname, freq from Stock natural join '
                   '(select count(userid) as freq, stockid from Watchlist '
                   'group by stockid having stockid in '
                   '(select stockid from Watchlist where UserId = '
                   '(select id from auth_user where username = %s))) a '
                   'order by freq desc, stockname asc', [request.user.username])
    rows = cursor.fetchall()
    cursor.callproc('Recommend')
    print(cursor.fetchall())
    freqs = []
    for i, r in enumerate(watchlist):
        freqs.append({'stockname': r.stockname, 'price': r.price, 'freq': rows[i][1]})
    return render(request, 'accounts/home.html', {'watchlist': freqs})


@login_required(login_url='login')
def update_password(request):
    err = None
    changeForm = PasswordChangeForm(request.user)
    if request.method == 'POST':
        changeForm = PasswordChangeForm(request.user, request.POST)
        user = User.objects.raw('select * from auth_user where username = %s', [request.user.username])
        old_password = user[0].password
        if old_password == changeForm.data['old_password']:
            password = changeForm.data['new_password1']
            cursor.execute('update auth_user set `password` = %s where username = %s', [password, request.user.username])
            messages.success(request, 'Password successfully changed')
            return redirect('logout')
        else:
            err = 'old password is incorrect'
    return render(request, 'accounts/update_password.html', {'changeForm': changeForm, 'err': err})


def delete_user(request):
    cursor.execute('delete from auth_user where username = %s', [request.user.username])
    messages.success(request, 'User ' + request.user.username + ' successfully deleted')
    return redirect('login')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            fn = form.cleaned_data['first_name']
            ln = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            cursor.execute('insert into auth_user (first_name, last_name, username, password, is_superuser, email, '
                           'is_staff, is_active, date_joined) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                           [fn, ln, username, password, 0, email, 1, 1, '2021-11-10'])
            messages.success(request, 'User create successful for ' + username)
            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.raw('select * from auth_user where username = %s and password = %s', [username, password])
        if len(user) > 0:
            user = user[0]
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username and password do not match')
            return render(request, 'accounts/login.html', {})
    return render(request, 'accounts/login.html', {})


def logout_view(request):
    logout(request)
    messages.info(request, 'User is logged out')
    return redirect('login')


def add_procedure():
    cursor.execute(
        '''
        create procedure Recommend()
begin
declare decreaseStock varchar(255);
declare increaseStock varchar(255);
declare favoriteStock varchar(255);
declare sn varchar(255);
declare fp real;
declare cp real;
declare diff real;
declare done boolean default false;

    	declare cur1 cursor for 
 (
       		select stockname, max_price, curr_price
from (select stockname, price as curr_price from Stock) a
natural join (select stockname, max(sp.price) as max_price from Stock s join StockPrice sp using(StockId) group by stockname) b
);
declare cur2 cursor for 
 (
       		select stockname, avg_price, curr_price
from (select stockname, price as curr_price from Stock) a
natural join (select stockname, avg(sp.price) as avg_price from Stock s join StockPrice sp using(StockId) group by stockname) b
);
declare cur3 cursor for 
 (
	select stockname from Stock join 
(
		select stockId, count(userId) as cnt 
		from Watchlist
		group by stockId
) a using(stockId)
order by cnt desc
limit 1
);

    	declare continue handler for not found set done = true;

	drop table if exists final;
   	create table final
    	(
        		id int,
        		stockname varchar(255)
    	);

    
	set diff = 0;
   	open cur1;
    	myloop: loop
        		if done then
            		leave myloop;
        		end if;
        		fetch cur1 into sn, fp, cp;
		
        		if fp - cp > diff then
            		set diff = fp - cp;
			set decreaseStock = sn;
        		end if;
    	end loop myloop;
    	close cur1;

	set diff = 0;
	set done = false;
   	open cur2;
    	myloop: loop
        		if done then
            		leave myloop;
        		end if;
        		fetch cur2 into sn, fp, cp;
		
        		if cp - fp > diff then
            		set diff = cp - fp;
			set increaseStock = sn;
        		end if;
    	end loop myloop;
    	close cur2;

    set done = false;
	open cur3;
    	myloop: loop
        		if done then
            		leave myloop;
        		end if;
        		fetch cur3 into favoriteStock;
    	end loop myloop;
    	close cur3;

	insert into final values(1, decreaseStock);
	insert into final values(2, increaseStock);
	Insert into final values(3, favoriteStock);

	select * from final order by id asc;
end
        '''
    )

# add_procedure()