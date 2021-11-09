from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.db import connection
from .forms import CreateUserForm
from .models import Stock


# Create your views here.
@login_required(login_url='login')
def home_view(request):
    watchlist = Stock.objects.raw('select * from Stock where stockid in '
                                  '(select stockid from Watchlist where UserId = '
                                  '(select id from auth_user where username = %s))', [request.user.username])
    cursor = connection.cursor()
    cursor.execute('select stockname, freq from Stock natural join '
                   '(select count(userid) as freq, stockid from Watchlist '
                   'group by stockid having stockid in '
                   '(select stockid from Watchlist where UserId = '
                   '(select id from auth_user where username = %s))) a '
                   'order by freq desc, stockname asc', [request.user.username])
    rows = cursor.fetchall()
    freqs = []
    for r in rows:
        freqs.append({'stockname': r[0], 'freq': r[1]})
    return render(request, 'accounts/home.html', {'watchlist': watchlist, 'freqs': freqs})


@login_required(login_url='login')
def update_password(request):
    changeForm = PasswordChangeForm(request.user)
    if request.method == 'POST':
        changeForm = PasswordChangeForm(request.user, request.POST)
        if changeForm.is_valid():
            user = changeForm.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password successfully changed')
            return redirect('logout')
    return render(request, 'accounts/update_password.html', {'changeForm': changeForm})


def delete_user(request):
    try:
        request.user.delete()
        messages.success(request, 'User ' + request.user.username + ' is successfully deleted.')

    except Exception as e:
        return render(request, 'accounts/home.html', {'err': e.message})

    return redirect('login')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
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
        user = authenticate(request, username=username, password=password)
        if user is not None:
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
