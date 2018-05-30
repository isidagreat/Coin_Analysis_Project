from django.shortcuts import render, HttpResponse, redirect
from time import gmtime, strftime
from datetime import date, datetime, time
from time import mktime
from .models import users, coin
from django.contrib import messages
import bcrypt, matplotlib, requests
import pandas as pd
import numpy as np
matplotlib.use('SVG')
import matplotlib.pyplot as plt, mpld3
import json
import requests
import simplejson as json
from statsmodels.formula.api import ols
from .write_json import * #dont need anymore
from .datetimecalculation import * #sids custom function
from .erikdatetimecalc import * #erik's custom function built on sids

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
                #print(key,value,category)
                messages.set_level(request,category) #otherwise will ignore add message
                messages.add_message(request, category, value)    
            #print('ERROR::',errors)
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
                #print(key,value,category)
                messages.add_message(request, category, value)    
            #print('ERROR::',errors)
            return redirect('/')
        else: #create user
            hash_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            user = users.objects.create(fname = request.POST['first_name'], lname = request.POST['last_name'], email = request.POST['email'], pw_hash = hash_pw)
            user_id = user.id
            request.session['create'] = True
            request.session['user_id'] = user_id
            #print('CREATED::', user)
            return redirect("/graphs")
    else:
        return redirect('/')

def show(request, id): #success page
    if request.session['user_id'] != -1: #user is here
        this_user = users.objects.get(id = str(id))
        #print('SHOW::',this_user)
        context = {'ID' : this_user.id,
                    'full_name' : (this_user.fname + ' ' + this_user.lname),
                    'email' : this_user.email,
                    'created_at' : this_user.created_at,
                    'iterator' : [1,2,3,4]
                   }
        request.session['first_name'] = this_user.fname
        return render(request,"django_app/user_graphs.html", context)
    else: #user is not here
        messages.add_message(request, 0, 'you must log in')
        return redirect('/users/login_page')

def edit_page(request, id): #edit page
    if request.session['user_id'] != -1: #user is here
        this_user = users.objects.get(id = str(id))
        #print('SHOW::',this_user)
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
            #print('ERROR::',errors)
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
        # Returns coin historical data for last 30 days
        data = coinHist('1', 30)
        data2 = coinHist('825', 30)
    else:
        messages.add_message(request, 0, 'you must log in')
        return redirect('/users/login_page')
    context = {
        'user' : users.objects.get(id = str(user_id)),
        #'coin1': json.dumps(data[:]),
        #'coin2': json.dumps(data2[:]),
    }
    print (context)
    return render(request, "django_app/coin_graphs_homepage.html", context)

def del_graph(request,user_id):
    if request.method == "POST":
        #os.remove() #removing a file in use in windows causes an exception to be raised
        #this means that we cannot dynamically use files to render graphs
        return redirect('/graphs')
       
    else:
        return redirect('/graphs')

def plot(request, graph_id): #pd = pandas #np = numpy #matplotlib = plt #statsmodels = ols
    if request.method == 'POST':
        user_id = str(request.session['user_id'])
        graph = int(graph_id)
        
        coin_x = coin_zero(request.POST['x_coin']) #processes which coin and gives appropriate variables
        coin_y = coin_zero(request.POST['y_coin'])
        x_zero = coin_x[0]
        y_zero = coin_y[0]
        
        range_is_different = range_equalizer(x_zero, y_zero) #validator for lower range of coin

        timestamp1 = unix_time(datetime.strptime(request.POST['start'], "%Y-%m-%d"))
        timestamp2 = unix_time(datetime.strptime(request.POST['end'], "%Y-%m-%d"))

        x_key = key_validation(request.POST['x_key'],'price')
        y_key = key_validation(request.POST['y_key'],'time')

        x_name = coin_x[1] + ' ' + x_key
        y_name = coin_y[1] + ' ' + y_key

        coin1_array = coinHistory(int(request.POST['x_coin']),timestamp1,timestamp2, x_zero)
        coin2_array = coinHistory(int(request.POST['y_coin']),timestamp1,timestamp2, y_zero)

        apply = request.POST['stat_func']

        if coin1_array != False and coin2_array != False: 
            x = axis(coin1_array, x_key)
            y = axis(coin2_array, y_key)
            this_user = user.get(id = int(user_id))
            this_plot = plot.objects.create(x_axis = x, y_axis = y, x_label = x_name, y_label = y_name, function = apply, user = this_user)
            #will plot in render
            # plotarr = [x,y] #2d array for plotting
            # fig = plt.figure(figsize=(3,2))
            # plt.plot(plotarr[0],plotarr[1])
            return redirect('/graphs/dashboard/'+user_id)
        else:
            return redirect('/users/'+user_id)
    else:
        return redirect('/users/'+user_id)
    #fig.savefig('./apps/first_app/static/django_app/img/examplebcplot' + str(graph_id) +'.svg', bbox_inches='tight') #saves the file to img folder
    # fig.fig_to_html()
    # plt.close(fig)
    return redirect('/users/'+user_id)

def axis(array,key_str): #this function searches a passed in array for the key_str and returns the array of only those values
    axis_var = [] #can be x or y usually
    for obj in array:
        axis_var.append(obj[key_str])
    return axis_var

def key_validation(key, default):
    if key != 'time' or key != 'price':
        key = default
    return key

def coin_zero(coin_id):
    if coin_id == '825':
        zero = 1424871266 #Tether Zero Time Unix
        name = 'Tether'
    elif coin_id == '1':
        zero = 1367174841 #Bitcoin Zero Time Unix
        name = 'BitCoin'
    else:
        zero = 1367174841
        name = 'BitCoin'
    output = [zero,name]
    return output

def range_equalizer(coin1,coin2): #true means function executed
    if coin1 < coin2: #this function makes sure the stats are analyzing the same range
        coin1 = coin2 #it will shorten the range to the latest created coin's first measurement
        return True
    elif coin2 < coin1:
        coin2 = coin1
        return True
    else: #they are equal
        return False

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
  
def coin(request, id,begin,end):
    # call coinHist function
    #data = coinHist(id, time)
    data = coinHistory(id,begin, end)
    if data == False:
        return redirect("/graphs")
    info = requests.get("https://api.coinmarketcap.com/v2/ticker/"+id)
    coin= info.json()
    context = {
        "coins": coin,
        "prices": json.dumps(data[:])
    }
    return render(request, "django_app/coin_page.html", context)

def dateRange(request,id): #dont need anymore
    start = request.POST['start']
    print (start)
    timestamp1= mktime(datetime.strptime(start, "%Y-%m-%d").timetuple())
    print (int(timestamp1))
    end =request.POST['end']
    print (end)
    timestamp2= mktime(datetime.strptime(end, "%Y-%m-%d").timetuple())
    print (int(timestamp2))

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
    datePrice =[]
    for i in range(0,len(data['price_usd'])):
        if datetime.fromtimestamp(int(timestamp1)).strftime('%Y-%m-%d') == datetime.fromtimestamp(int((data['price_usd'][i][0])/1000)).strftime('%Y-%m-%d'):
            count = i
            while datetime.fromtimestamp(int(timestamp2)).strftime('%Y-%m-%d') != datetime.fromtimestamp(int((data['price_usd'][count][0]))/1000).strftime('%Y-%m-%d'):
                times = datetime.fromtimestamp(int((data['price_usd'][count][0])/1000)).strftime('%Y-%m-%d')
                price = data['price_usd'][count][1]
                datePrice.append({'time': times,'price': price})
                count += 1
        else:
            pass
    if data == False:
        return redirect("/")
    info = requests.get("https://api.coinmarketcap.com/v2/ticker/"+id)
    coin= info.json()
    context = {
        "coins": coin,
        "prices": json.dumps(datePrice[:])
    }

    return render(request,"django_app/coin_page.html", context )
def logout(request):
    request.session.clear()
    return redirect('/users')

def correlation(request):
    col1 = [1,2,3,4,5]
    col2 = [1,2,3,4,5]
    col1.corr(col2)
    return redirect('/graph')

