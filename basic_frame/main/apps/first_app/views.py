from django.shortcuts import render, HttpResponse, redirect
from time import gmtime, strftime
from datetime import date, datetime
from .models import users
from django.contrib import messages
import bcrypt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import requests
from statsmodels.formula.api import ols
from .write_json import *
from .datetimecalculation import *

def index(request):
    if 'initial' in request.session: #allows me to do things on initialization
        request.session['initial'] = False
        if request.session['user_id'] != -1: #user is here
            messages.error(request,'you are logged in')
            return redirect('/users/'+str(request.session['user_id'])) #keeps them logged in
        #print(request.session)
    else:
        request.session['initial'] = True #initialize default values for session to avoid checking if they are in later
        request.session['user_id'] = -1 #on login makes a different user id
        request.session['create'] = False #turns true on successful registration
    return render(request, "django_app/registration.html")

def login_page(request):
    if 'initial' in request.session: #reinitializes on login redirect. clearing the cookie will end up here again
        request.session['initial'] = False
        if request.session['user_id'] != -1: #user is here
            messages.error(request,'you are logged in')
            return redirect('/users/'+str(request.session['user_id'])) #keeps them logged in
        #print(request.session)
    else:
        request.session['initial'] = True #initialize default values for session to avoid checking if they are in later
        request.session['user_id'] = -1 #on login makes a different user id
        request.session['create'] = False #turns true on successful registration
    return render(request,"django_app/login.html")

def login(request):
    if request.method == 'POST':
        errors = users.objects.login_validator(request.POST)
        category = 0
        key_prev = 'j'
        if len(errors):
            for key,value in errors.items():
                if key_prev != key: #allows for multiple errors to display over one box
                    key_prev = key
                    category += 1               
                print(key,value,category)
                messages.set_level(request,category) #otherwise will ignore add message
                messages.add_message(request, category, value)    
            print('ERROR::',errors)
            return redirect('/users/login_page')
        else: #no errors passed credentials true
            userID = users.objects.get(email = request.POST['email']).id
            request.session['user_id'] = userID
            return redirect("/users/"+str(userID))            
    else:
        return redirect('/users/login_page')
        
def create(request): #user registration
    if request.method == "POST":
        errors = users.objects.user_validator(request.POST)
        category=0
        key_prev = 'j'
        if len(errors):
            for key,value in errors.items():
                messages.set_level(request,category) #otherwise will ignore add message
                if key_prev != key: #allows for multiple errors to display over one box
                    key_prev = key
                    category += 1
                print(key,value,category)
                messages.add_message(request, category, value)    
            print('ERROR::',errors)
            return redirect('/')
        else: #create user
            hash_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            user = users.objects.create(fname = request.POST['first_name'], lname = request.POST['last_name'], email = request.POST['email'], pw_hash = hash_pw)
            user_id = user.id
            request.session['create'] = True
            request.session['user_id'] = user_id
            print('CREATED::', user)
            return redirect("/graphs")
    else:
        return redirect('/')

def show(request, id): #success page
    if request.session['user_id'] != -1: #user is here
        this_user = users.objects.get(id = str(id))
        print('SHOW::',this_user)
        context = {'ID' : this_user.id,
                    'full_name' : (this_user.fname + ' ' + this_user.lname),
                    'email' : this_user.email,
                    'created_at' : this_user.created_at,
                   }
        request.session['first_name'] = this_user.fname
        return render(request,"django_app/user_graphs.html", context)
    else: #user is not here
        messages.add_message(request, 0, 'you must log in')
        return redirect('/users/login_page')

def edit_page(request, id): #edit page
    if request.session['user_id'] != -1: #user is here
        this_user = users.objects.get(id = str(id))
        print('SHOW::',this_user)
        context = {'ID' : this_user.id,
                    'first_name' : this_user.fname,
                    'last_name' : this_user.lname,
                    'email' : this_user.email,
                    'created_at' : this_user.created_at}
        request.session['first_name'] = this_user.fname
        return render(request,"django_app/user_edit.html", context)
    else: #user is not here
        messages.add_message(request, 0, 'you must log in')
        return redirect('/users/login_page')

def edit_user(request):
    if request.session['user_id'] != -1:
        user_id = request.session['user_id']
    else:
        messages.add_message(request, 0, 'you must log in')
        return redirect('/users/login_page')
    if request.method == "POST":
        errors = users.objects.edit_validator(request.POST)
        category=0
        key_prev = 'j'
        if len(errors):
            for key,value in errors.items():
                messages.set_level(request,category) #otherwise will ignore add message
                if key_prev != key: #allows for multiple errors to display over one box
                    key_prev = key
                    category += 1
                print(key,value,category)
                messages.add_message(request, category, value)    
            print('ERROR::',errors)
            return redirect("/users/"+str(user_id)+'/edit')
        else: #update user
            this_user = users.objects.get(id = str(user_id))
            this_user.fname = request.POST['first_name']
            this_user.lname = request.POST['last_name']
            this_user.email = request.POST['email']
            this_user.save() #put into DB
            return redirect("/users/"+str(user_id))
    else:
        return redirect('/')

def dashboard(request):
    if request.session['user_id'] != -1:
        user_id = request.session['user_id']
    else:
        messages.add_message(request, 0, 'you must log in')
        return redirect('/users/login_page')
    context = {
        'user' : users.objects.get(id = str(user_id))
    }
    return render(request, "django_app/coin_graphs_homepage.html", context)

def addquote(request,user_id):
    if request.method == "POST":
        # errors = quotes.objects.quote_validator(request.POST)
        # category=0
        # key_prev = 'j'
        # if len(errors):
        #     for key,value in errors.items():
        #         messages.set_level(request,category) #otherwise will ignore add message
        #         if key_prev != key: #allows for multiple errors to display over one box
        #             key_prev = key
        #             category += 1
        #         print(key,value,category)
        #         messages.add_message(request, category, value)
        #     print('ERROR::',errors)
        return redirect('/graphs')
        # else: #create quote
        #     # poster = users.objects.get(id = user_id)
        #     # print(poster)
        #     # this_quote = quotes.objects.create(quotee = request.POST['quotee'], quote = request.POST['quote'], poster = poster) #poster likes his own posts automatically
        #     return redirect('/graphs')
    else:
        return redirect('/graphs')

def correlate(request,graph_id):
    user_id = str(request.session['user_id'])
    graph = int(graph_id)
    x = np.linspace(-5,5,20)
    np.random.seed(graph)
    y = -5 + 3*x + 4 *np.random.normal(size=x.shape)
    plt.figure(figsize=(5,4)) #random figure with an up correlation
    plt.plot(x,y,'o')
    plt.figure().savefig('exampleplot'+ str(graph_id) +'.svg') #saves the file
    return redirect('/users/'+user_id)

def like(request,user_id,quote_id):
    if request.method == 'POST':
        return redirect('/graphs')
    else:
        return redirect('/graphs')

def graph_interface(request,user_id):
    context = {
        "user_id" : user_id
    }
    return render(request, 'django_app/create_graph.html', context)

def coin(request, id,time):
    # call coinHist function
    data = coinHist(id, time)
    if data == False:
        return redirect("/")
    info = requests.get("https://api.coinmarketcap.com/v2/ticker/"+id)
    coin= info.json()
    context = {
        "coins": coin,
        "prices": json.dumps(data[:])
    }
    return render(request, "django_app/coin_page.html", context)

def dateRange(request,id):
    start = request.POST['start']
    print (start)
    timestamp1= time.mktime(datetime.strptime(start, "%Y/%m/%d").timetuple())
    print (timestamp1)
    request.POST['end']

    if id == '825':
        URL = "https://graphs2.coinmarketcap.com/currencies/tether/"
    elif id == '1':
        URL = "https://graphs2.coinmarketcap.com/currencies/bitcoin/"
    else:
        return redirect("/")
    # Create GET request to API
    response = requests.get(URL)
    # Translate to JSON
    data = response.json()
    # Storing date and price into Object List
    totals = len(data['price_usd'])
    
    for i in range(span,len(data['price_usd'])):
        times = datetime.fromtimestamp(int((data['price_usd'][i][0])/1000)).strftime('%Y-%m-%d')
        price = data['price_usd'][i][1]
        datePrice.append({'time': times,'price': price})
    return redirect("/coin/"+id+"/"+365)

def logout(request):
    request.session.clear()
    return redirect('/users')

def correlation(request):
    col1 = [1,2,3,4,5]
    col2 = [1,2,3,4,5]
    col1.corr(col2)
    return redirect('/graph')
