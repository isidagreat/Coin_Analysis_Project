import requests
from datetime import date, datetime
def coinHist(id,time):
  # Find specific coin wanted through id
    if id == '825':
        URL = "https://graphs2.coinmarketcap.com/currencies/tether/"
    elif id == '1':
        URL = "https://graphs2.coinmarketcap.com/currencies/bitcoin/"
    else:
        return False
    # Create GET request to API
    response = requests.get(URL)
    # Translate to JSON
    data = response.json()
    # Storing date and price into Object List
    totals = len(data['price_usd'])
    if int(time) == 0 or int(time) < 0:
        span = 0
    elif int(time) > totals:
        span = 0
    else:
        span = totals - int(time)
    datePrice = []
    for i in range(span,len(data['price_usd'])):
        time = datetime.fromtimestamp(int((data['price_usd'][i][0])/1000)).strftime('%Y-%m-%d')
        price = data['price_usd'][i][1]
        datePrice.append({'time': time,'price': price})
        # return the objectList
    return datePrice