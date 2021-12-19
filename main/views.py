from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core import serializers
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.validators import validate_email
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.views import View
from django.views.generic import RedirectView
from .models import User

import numpy as np
from tensorflow import keras
from sklearn.preprocessing import StandardScaler
import os
from pathlib import Path

# from .forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
import requests
from .utils import token_gen
import requests
import json

import datetime

def main(request):
	return render(request, 'main/index.html')

def register(request):
	context = {'error': ""}
	if request.method == 'POST':
		if request.POST.get('password1') == request.POST.get('password2'):
			password = request.POST.get('password1')
			name = request.POST.get('Name')
			surname = request.POST.get('Surname')
			if not validate_email(request.POST.get('Email')):
				email = request.POST.get('Email')
			else:
				print("Not a valid Email")
				return render(request, 'main/register.html', context)
			usr = User(name = name, surname=surname, email = email, password=password)
			usr.save()
			return redirect("/")
		else:
			print("Passwords Don't Match")
			return render(request, 'main/register.html', context)
	else:
		print(request.method)
		return render(request, 'main/register.html', context)

class account_activated(View):
	def get(self, request, uidb64, token):
		try:
			uid = force_text(urlsafe_base64_decode(uidb64))
			user = User.objects.get(pk=uid)
		except Exception as identifier:
			user = None
		if user is not None and token_gen.check_token(user, token):
			user.is_active = True
			user.save()
			messages.add_message(request, messages.SUCCESS, 'Account activated succesfully!')
			login(request, user)
			return redirect('homepage')
		return render(request, 'main/mails/activation_failed.html', status=401)

def logout_user(request):
	logout(request)
	return redirect('/')

def login(request):
	context = {'error': ""}
	if request.method == 'POST':
		blog = User.objects.filter(email=request.POST.get('email'), password=request.POST.get('password'))
		if(len(blog) == 1):
			blog.update(is_authenticated=True)
			return redirect("/")
		elif(len(blog) > 1):
			context["error"] = "More than one concurrent accounts found.."
		else:
			context["error"] = "Incorrect Email/Password, cound not find account..."

		return render(request, 'main/index.html', context)
	else:
		return render(request, 'main/login.html', context)

def PersonalFinance(request):
	User.objects.filter(is_authenticated=True).update(today = datetime.datetime.now())
	if (User.objects.filter(is_authenticated=True)[0].today - User.objects.filter(is_authenticated=True)[0].last_earning_add).days > 30:
		User.objects.filter(is_authenticated=True).update(savings=str(float(User.objects.filter(is_authenticated=True)[0].savings)+float(User.objects.filter(is_authenticated=True)[0].monthly_earnings)))
		User.objects.filter(is_authenticated=True).update(saving_history=str(User.objects.filter(is_authenticated=True)[0].saving_history) + " " + str(float(User.objects.filter(is_authenticated=True)[0].savings)+float(User.objects.filter(is_authenticated=True)[0].monthly_earnings)))
		User.objects.filter(is_authenticated=True).update(last_earning_add=User.objects.filter(is_authenticated=True)[0].today)
		 
	context={"expense":0, "time_left": "Submit form to calculate expense first"}
	if request.method == "POST":
		expense = float(request.POST.get("misc"))+float(request.POST.get("rent"))+float(request.POST.get("water"))+float(request.POST.get("electricity"))+float(request.POST.get("food"))+float(request.POST.get("clothing"))+float(request.POST.get("transport"))
		User.objects.filter(is_authenticated=True).update(transport_expenses=request.POST.get("transport"))
		User.objects.filter(is_authenticated=True).update(clothing_expenses=request.POST.get("clothing"))
		User.objects.filter(is_authenticated=True).update(food_expenses=request.POST.get("food"))
		User.objects.filter(is_authenticated=True).update(electricity_expenses=request.POST.get("electricity"))
		User.objects.filter(is_authenticated=True).update(water_expenses=request.POST.get("water"))
		User.objects.filter(is_authenticated=True).update(rent_expenses=request.POST.get("rent"))
		User.objects.filter(is_authenticated=True).update(misc_expenses=request.POST.get("misc"))
		User.objects.filter(is_authenticated=True).update(expenses=User.objects.filter(is_authenticated=True)[0].expenses + " " + str(expense))
		User.objects.filter(is_authenticated=True).update(savings=str(float(User.objects.filter(is_authenticated=True)[0].savings)-expense))
		User.objects.filter(is_authenticated=True).update(saving_history=User.objects.filter(is_authenticated=True)[0].saving_history+" "+str(float(User.objects.filter(is_authenticated=True)[0].savings)-expense))
		context["expense"] = expense
		print(expense)
		current_expenses = float(User.objects.filter(is_authenticated=True)[0].expenses.split(" ")[-1])
		current_savings = float(User.objects.filter(is_authenticated=True)[0].savings)
		d = current_savings - current_expenses
		j = 1
		while d > 0:
			d = d - current_expenses
			j+=1
			if(d<5124):
				break
		context["time_left"] = j

	if len(User.objects.filter(is_authenticated=True)) == 1:
		context["savings"] = float(User.objects.filter(is_authenticated=True)[0].savings)
		context["expenseGraph"] = []
		context["User"] = User.objects.filter(is_authenticated=True)[0]
		context["expenses"] = User.objects.filter(is_authenticated=True)[0].expenses.split(" ")
		print(context["expenses"])
		for i in User.objects.filter(is_authenticated=True)[0].saving_history.split(" "):
			context["expenseGraph"].append(float(i))
		return render(request, "main/personal_finance.html", context)
	else:
		return redirect("/login/")

	model_AMZN = keras.models.load_model("main/models/stonks_AMZN.h5")
	model_AAPL = keras.models.load_model("main/models/stonks_AAPL.h5")
	model_FB = keras.models.load_model("main/models/stonks_FB.h5")
	model_GOOGL = keras.models.load_model("main/models/stonks_GOOGL.h5")
	model_TSLA = keras.models.load_model("main/models/stonks_TSLA.h5")
	model_ADA = keras.models.load_model("main/models/crypto_model_ADA.h5")
	model_BTC = keras.models.load_model("main/models/crypto_model_BTC.h5")
	model_DOGE = keras.models.load_model("main/models/crypto_model_DOGE.h5")
	model_ETH = keras.models.load_model("main/models/crypto_model_ETH.h5")


	finally_prediction_AMZN = model_AMZN.predict(np.array([3478.05], ndmin=3))
	finally_prediction_AAPL = model_AAPL.predict(np.array([154.30], ndmin=3))
	finally_prediction_FB = model_FB.predict(np.array([376.26], ndmin=3))
	finally_prediction_GOOGL = model_GOOGL.predict(np.array([2874.79], ndmin=3))
	finally_prediction_TSLA = model_TSLA.predict(np.array([733.57], ndmin=3))
	finally_prediction_ADA = model_AAPL.predict(np.array([1.27], ndmin=3))
	finally_prediction_BTC = model_FB.predict(np.array([49987.42], ndmin=3))
	finally_prediction_DOGE = model_GOOGL.predict(np.array([0.300228], ndmin=3))
	finally_prediction_ETH = model_TSLA.predict(np.array([3898.41], ndmin=3))

	current_savings = int(User.objects.filter(is_authenticated=True)[0].savings)
	if (current_savings < 100):
		context["invest_scheme"] = "Invest in Doge (Crypto)"
	elif(current_savings < 500):
		context["invest_scheme"] = "Invest in Ada (Crypto)"
	elif(current_savings < 3000):
		context["invest_scheme"] = "Invest in Ada and FB"
	elif(current_savings < 5000):
		context["invest_scheme"] = "Invest in AAPL"
	elif(current_savings < 10000):
		context["invest_scheme"] = "Invest in ETH and FB"
	elif(current_savings < 12000):
		context["invest_scheme"] = "Invest in Eth TSLA"
	elif(current_savings < 15000):
		context["invest_scheme"] = "Invest in ETH and GOOGL"
	elif(current_savings < 18000):
		context["invest_scheme"] = "Invest in Eth and AMZN"
	elif(current_savings < 20000):
		context["invest_scheme"] = "Invest in BTC"
	elif(current_savings < 25000):
		context["invest_scheme"] = "Invest in BTC and GOOGL"
	elif(current_savings > 30000):
		context["invest_scheme"] = "Invest in BTC and AMZN"
	elif(current_savings > 50000):
		context["invest_scheme"] = "Invest in BTC, AMZN and AAPL"
	

	context["AMZN"] = finally_prediction_AMZN[0][0]*1000
	context["AAPL"] = finally_prediction_AAPL[0][0]*1000
	context["FB"] = finally_prediction_FB[0][0]*1000
	context["GOOGL"] = finally_prediction_GOOGL[0][0]*1000
	context["TSLA"] = finally_prediction_TSLA[0][0]*1000
	context["ADA"] = finally_prediction_ADA[0][0]*1000
	context["BTC"] = finally_prediction_BTC[0][0]*1000
	context["DOGE"] = finally_prediction_DOGE[0][0]*1000
	context["ETH"] = finally_prediction_ETH[0][0]*1000

	return render(request, "main/personal_finance.html", {})

def news(request):
	context = {}
	itms = []
	news = requests.get("https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey=1295bd076efb4e53a87c25cf2bc6876b").json()["articles"]
	for i in news:
		itms.append("~".join([str(i["source"]["name"]), str(i["author"]), str(i["title"]), str(i["description"]), str(i["url"]), str(i["content"])]))
	context["news"] = "``".join(itms)
	return render(request, "main/news.html", context)

def predict(request):
	context = {}
	model_AMZN = keras.models.load_model("main/models/stonks_AMZN.h5")
	model_AAPL = keras.models.load_model("main/models/stonks_AAPL.h5")
	model_FB = keras.models.load_model("main/models/stonks_FB.h5")
	model_GOOGL = keras.models.load_model("main/models/stonks_GOOGL.h5")
	model_TSLA = keras.models.load_model("main/models/stonks_TSLA.h5")
	model_ADA = keras.models.load_model("main/models/crypto_model_ADA.h5")
	model_BTC = keras.models.load_model("main/models/crypto_model_BTC.h5")
	model_DOGE = keras.models.load_model("main/models/crypto_model_DOGE.h5")
	model_ETH = keras.models.load_model("main/models/crypto_model_ETH.h5")


	finally_prediction_AMZN = model_AMZN.predict(np.array([3478.05], ndmin=3))
	finally_prediction_AAPL = model_AAPL.predict(np.array([154.30], ndmin=3))
	finally_prediction_FB = model_FB.predict(np.array([376.26], ndmin=3))
	finally_prediction_GOOGL = model_GOOGL.predict(np.array([2874.79], ndmin=3))
	finally_prediction_TSLA = model_TSLA.predict(np.array([733.57], ndmin=3))
	finally_prediction_ADA = model_AAPL.predict(np.array([1.27], ndmin=3))
	finally_prediction_BTC = model_FB.predict(np.array([49987.42], ndmin=3))
	finally_prediction_DOGE = model_GOOGL.predict(np.array([0.300228], ndmin=3))
	finally_prediction_ETH = model_TSLA.predict(np.array([3898.41], ndmin=3))

	current_savings = int(User.objects.filter(is_authenticated=True)[0].savings)
	if (current_savings < 100):
		context["invest_scheme"] = "Invest in Doge (Crypto)"
	elif(current_savings < 500):
		context["invest_scheme"] = "Invest in Ada (Crypto)"
	elif(current_savings < 3000):
		context["invest_scheme"] = "Invest in Ada and FB"
	elif(current_savings < 5000):
		context["invest_scheme"] = "Invest in AAPL"
	elif(current_savings < 10000):
		context["invest_scheme"] = "Invest in ETH and FB"
	elif(current_savings < 12000):
		context["invest_scheme"] = "Invest in Eth TSLA"
	elif(current_savings < 15000):
		context["invest_scheme"] = "Invest in ETH and GOOGL"
	elif(current_savings < 18000):
		context["invest_scheme"] = "Invest in Eth and AMZN"
	elif(current_savings < 20000):
		context["invest_scheme"] = "Invest in BTC"
	elif(current_savings < 25000):
		context["invest_scheme"] = "Invest in BTC and GOOGL"
	elif(current_savings > 30000):
		context["invest_scheme"] = "Invest in BTC and AMZN"
	elif(current_savings > 50000):
		context["invest_scheme"] = "Invest in BTC, AMZN and AAPL"
	

	context["AMZN"] = finally_prediction_AMZN[0][0]*1000
	context["AAPL"] = finally_prediction_AAPL[0][0]*1000
	context["FB"] = finally_prediction_FB[0][0]*1000
	context["GOOGL"] = finally_prediction_GOOGL[0][0]*1000
	context["TSLA"] = finally_prediction_TSLA[0][0]*1000
	context["ADA"] = finally_prediction_ADA[0][0]*1000
	context["BTC"] = finally_prediction_BTC[0][0]*1000
	context["DOGE"] = finally_prediction_DOGE[0][0]*1000
	context["ETH"] = finally_prediction_ETH[0][0]*1000

	return render(request, 'main/foo.html', context)

def precautions(request):
	context = {}
	return render(request, "main/precautions.html", context)