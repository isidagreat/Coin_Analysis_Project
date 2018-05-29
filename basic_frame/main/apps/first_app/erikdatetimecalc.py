import requests
from datetime import date, datetime
def coinHistory(id,begin_time, end_time):
  # Find specific coin wanted through id
    if id == '825':
        URL = "https://graphs2.coinmarketcap.com/currencies/tether/"
    elif id == '1':
        URL = "https://graphs2.coinmarketcap.com/currencies/bitcoin/"
    else:
        URL = "https://graphs2.coinmarketcap.com/currencies/bitcoin/"
    # Create GET request to API
    response = requests.get(URL)
    # Translate to JSON
    data = response.json()
    if data.status_code != requests.code.ok: #checks if get/json was successful
        return False
    # Storing date and price into Object List
    max_len = int(len(data['price_usd']))

    #begin_time validation
    if type(begin_time) != type(1):
        begin_time = 0
    elif begin_time < 0: #when placing the first boundary, it needs to be between the max length-1 and 0 only
        begin_time = 0
    elif begin_time > max_len:
        begin_time = max_len - 1
    else:
        pass #valid placement, begin time is now for sure a valid input, and we can use it as a measurement below

    #end_time validation
    if type(end_time) != type(1):
        end_time = max_len
    elif end_time > max_len): #when placing the second boundary, it needs to be after begin_time and before max length
        end_time = max_len #max range
    elif end_time < begin_time:
        end_time = begin_time + 1 #min range
    else:
        pass #valid placement, we now have all valid inputs

    datePrice = []
    for i in range(begin_time,end_time): #organize data
        time = datetime.fromtimestamp(int((data['price_usd'][i][0])/1000)).strftime('%Y-%m-%d')
        price = data['price_usd'][i][1]
        datePrice.append({'time': time,'price': price})
        # return the objectList
    return datePrice