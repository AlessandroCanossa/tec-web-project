from hashlib import new
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.forms import PasswordChangeForm
from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from users.forms import UsernameChangeForm, UserForm
from users.models import User


def register(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        form = UserForm()
        context = {
            'form': form
        }
        return render(request, 'registration/signup.html', context)

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')
        else:
            context = {
                'form': form,
            }
            return render(request, 'registration/signup.html', context)


@login_required(login_url='users:login')
def settings(request: HttpRequest) -> HttpResponse:
    user = User.objects.get(pk=request.user.id)

    if request.method == 'GET':
        library = user.library_set.all()

        comments = user.comment_set.order_by('-created_on')

        history = user.readhistory_set.order_by('-date')

        buy_list = user.buylist_set.order_by('-date')

        my_comics = user.comic_set.all()

        context = {
            'lib_comics': library,
            'comments': comments,
            'history': history,
            'buy_list': buy_list,
            'my_comics': my_comics
        }

        return render(request, 'users/settings.html', context)


@login_required(login_url='users:login')
def market(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        user = User.objects.get(pk=request.user.id)
        try:
            amount = int(request.POST.get('coins_amount'))

            if amount <= 0:
                raise ValueError
        except ValueError:
            message = 'Insert a valid amount of coins'
            return HttpResponse(message, status=400)
        user.coinspurchase_set.create(coins=amount)
        user.coins += amount
        user.save()

        message = f"Successfully purchased {amount} coins"

        return HttpResponse(message, status=200)
    else:
        return render(request, 'users/market.html')


@login_required(login_url='users:login')
def change_username(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        user: User = User.objects.get(pk=request.user.id)
        try:
            form = UsernameChangeForm(request.POST)
            if form.is_valid():
                new_username = form.cleaned_data['username']
                user.username = new_username
                user.save()
            else:
                return HttpResponse('Invalid username', status=400)
        except IntegrityError:
            return HttpResponse('Username already taken', status=400)

        return HttpResponse('Username changed successfully', status=200)


@login_required(login_url='users:login')
def change_password(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        user = User.objects.get(pk=request.user.id)

        form = PasswordChangeForm(user, request.POST)

        if form.is_valid():
            form.save()
            return HttpResponse('Password changed successfully', status=200)

        else:
            return HttpResponse(form.error_messages, status=400)


@login_required(login_url='users:login')
def become_creator(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        user = User.objects.get(pk=request.user.id)

        if user.is_creator:
            return HttpResponse('You are already a creator', status=400)

        user.is_creator = True
        user.groups.add(Group.objects.get(name='creator'))
        user.save()
        return HttpResponse('You are now a creator', status=200)
