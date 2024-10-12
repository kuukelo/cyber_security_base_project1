from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.db import transaction
from .models import Account
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login, authenticate
import os
import sys
import sqlite3
import logging
from django.conf import settings

@login_required
def addView(request):

	fmt = getattr(settings, 'LOG_FORMAT', None)
	lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)

	logging.basicConfig(format=fmt, level=lvl)
	logging.debug("Logging started on %s for %s" % (logging.root.name, logging.getLevelName(lvl)))
	logging.debug("Oh hai!")

	user = request.user
	ib = request.POST.get('iban')
	id = int(user.id)
	logging.debug(id)
	logging.debug(user.id+user.id)
	if ib != "":
	# 	new = Account.objects.create(owner = user, iban = ib, balance = 0)
		
		iban_ok = True
		# for c in ib:
		# 	if c not in ["0123456789"]:
		# 		iban_ok = False
		# 		break

		if iban_ok:
			SERVER_DIR = 'src'
			conn = sqlite3.connect(SERVER_DIR + '/db.sqlite3')
			cursor = conn.cursor()
			query = f"INSERT INTO pages_account (iban, balance, owner_id) VALUES('{str(ib)}',0,{user.id});"
			cursor.execute(query)
			conn.commit()
	return redirect('/')

@login_required
@csrf_exempt
def transferView(request):
	# with transaction.atomic():
	user = request.user
	if request.method == 'POST':
		sender = Account.objects.get(iban=request.POST.get('from'))
		receiver = Account.objects.get(iban=request.POST.get('to'))
		amount = int(request.POST.get('amount'))

		# if sender.balance >= amount and amount > 0 and sender != receiver and sender.owner == user:
		receiver.balance += amount
		sender.balance -= amount

		sender.save()
		receiver.save()

	return redirect('/')

@login_required
def homePageView(request):
	ownaccounts = Account.objects.filter(owner=request.user)
	allaccounts = Account.objects.all()
	return render(request, 'pages/index.html', {'accounts': ownaccounts, 'all': allaccounts})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'pages/signup.html', {'form': form})