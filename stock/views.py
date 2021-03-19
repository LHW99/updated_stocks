from django.shortcuts import render
from django.http import HttpResponse
from django.urls.base import reverse
try:
  from updated_stocks.settings.private_settings import CLOUD_API_KEY
except:
  from updated_stocks.settings.api import CLOUD_API_KEY
import requests
from stock_dataframe import rv_dataframe
import matplotlib.pyplot as plt
from matplotlib import style
import io
import urllib, base64

def index(request):
  if request.method == 'GET':
    try:
      # to get the ticker information
      ticker = request.GET['ticker_search']
      symbol = ticker.upper()
      response = requests.get(f'https://sandbox.iexapis.com/stable/stock/market/batch?symbols={symbol}&types=quote,stats,advanced-stats&token={CLOUD_API_KEY}')
      data = response.json()

      # to get ticker chart information
      chart_response = requests.get(f'https://sandbox.iexapis.com/stable/stock/{symbol}/chart/1y?token={CLOUD_API_KEY}')
      chart_data = chart_response.json()

      num = list(range(0, len(chart_data)))
      
      def testing():
        dictionary = []
        for row in num:
          dictionary.append(chart_data[row]['close'])
        return dictionary

      # chart plotting
      plt.style.use('dark_background')
      plt.clf()
      plt.plot(num, testing(), color='#0dba86')
      plt.title('Past Year Performance')
      plt.xlabel('Time')
      plt.ylabel('Share Price')
      plt.tick_params(labelbottom='off')

      fig = plt.gcf()
      buf = io.BytesIO()
      fig.savefig(buf, format='png')
      buf.seek(0)
      string = base64.b64encode(buf.read())

      uri = 'data:image/png;base64,' + urllib.parse.quote(string)

      plt.close

      return render(request, 'index.html', {
      'companyName': data[symbol]['quote']['companyName'],
      'symbol': f'({symbol})',
      'latestPrice': f"${data[symbol]['quote']['latestPrice']}",
      'marketCap': f"Market Cap (Billions): {data[symbol]['quote']['marketCap']/1000000000:.2f}",
      'month1ChangePercent': f"1-Month Percentage Change: {data[symbol]['stats']['month1ChangePercent']*100:.2f}%",
      'month3ChangePercent': f"3-Month Percentage Change: {data[symbol]['stats']['month3ChangePercent']*100:.2f}%",
      'month6ChangePercent': f"6-Month Percentage Change: {data[symbol]['stats']['month6ChangePercent']*100:.2f}%",
      'year1ChangePercent': f"1-Year Percentage Change: {data[symbol]['stats']['year1ChangePercent']*100:.2f}%",  
      'week52High': f"52-Week High: ${data[symbol]['quote']['week52High']}",
      'week52Low': f"52-Week Low: ${data[symbol]['quote']['week52Low']}",
      'peRatio': f"Price-to-Earnings Ratio: {data[symbol]['quote']['peRatio']}",
      'priceToBook': f"Price-to-Book Ratio: {data[symbol]['advanced-stats']['priceToBook']}",
      'priceToSales': f"Price-to-Sales Ratio: {data[symbol]['advanced-stats']['priceToSales']}",
      'chart': uri,
      })
    except:
      return render(request, 'index.html')
  
  else: 
    return HttpResponse('index')

  return render(request, 'index.html')

def top50gain(request):
  if request.method == 'GET':
    try:
      time = request.GET.get('timer')
      df = rv_dataframe
      df.sort_values(f"Percentage Change ({time})", ascending = False, inplace = True)
      df = df[:50]
      df.reset_index(drop = True, inplace = True)
      df = df.to_html(index=False)
      return render(request, 'top50gain.html', {'df': df})
    except:
      df = rv_dataframe
      df.sort_values('Percentage Change (5-Years)', ascending = False, inplace = True)
      df = df[:50]
      df.reset_index(drop = True, inplace = True)
      df = df.to_html(index=False)
      return render(request, 'top50gain.html', {'df': df})

  return render(request, 'top50gain.html', {'df': df})

def top50loss(request):
  if request.method == 'GET':
    try:
      time = request.GET.get('timer')
      df = rv_dataframe
      df.sort_values(f"Percentage Change ({time})", ascending = True, inplace = True)
      df = df[:50]
      df.reset_index(drop = True, inplace = True)
      df = df.to_html(index=False)
      return render(request, 'top50loss.html', {'df': df})
    except:
      df = rv_dataframe
      df.sort_values('Percentage Change (5-Years)', ascending = True, inplace = True)
      df = df[:50]
      df.reset_index(drop = True, inplace = True)
      df = df.to_html(index=False)
      return render(request, 'top50loss.html', {'df': df})

  return render(request, 'top50loss.html', {'df': df})

def top50pe(request):
  df = rv_dataframe
  df.sort_values('P/E Ratio', ascending = False, inplace = True)
  df = df[:50]
  df.reset_index(drop = True, inplace = True)
  df = df.to_html(index=False)

  return render(request, 'top50pe.html', {'df': df})

def all(request):
  df = rv_dataframe.to_html(index=False)

  return render(request, 'all.html', {'df': df})

def compare(request):
  if request.method == 'GET':
    try:
      # to get the ticker information
      ticker1 = request.GET['compare1']
      ticker2 = request.GET['compare2']
      symbol1 = ticker1.upper()
      symbol2 = ticker2.upper()
      response = requests.get(f'https://sandbox.iexapis.com/stable/stock/market/batch?symbols={symbol1},{symbol2}&types=quote,stats,advanced-stats&token={CLOUD_API_KEY}')
      data = response.json()

      return render(request, 'compare.html', {
      'companyName1': data[symbol1]['quote']['companyName'],
      'companyName2': data[symbol2]['quote']['companyName'],
      'symbol1': f'({symbol1})',
      'symbol2': f'({symbol2})',
      'latestPrice1': f"${data[symbol1]['quote']['latestPrice']}",
      'latestPrice2': f"${data[symbol2]['quote']['latestPrice']}",
      'marketCap1': f"Market Cap (Billions): {data[symbol1]['quote']['marketCap']/1000000000:.2f}",
      'marketCap2': f"Market Cap (Billions): {data[symbol2]['quote']['marketCap']/1000000000:.2f}",
      'year1ChangePercent1': f"1-Year Percentage Change: {data[symbol1]['stats']['year1ChangePercent']*100:.2f}%",  
      'year1ChangePercent2': f"1-Year Percentage Change: {data[symbol2]['stats']['year1ChangePercent']*100:.2f}%",  
      'week52High1': f"52-Week High: ${data[symbol1]['quote']['week52High']}",
      'week52High2': f"52-Week High: ${data[symbol2]['quote']['week52High']}",
      'week52Low1': f"52-Week Low: ${data[symbol1]['quote']['week52Low']}",
      'week52Low2': f"52-Week Low: ${data[symbol2]['quote']['week52Low']}",
      'peRatio1': f"Price-to-Earnings Ratio: {data[symbol1]['quote']['peRatio']}",
      'peRatio2': f"Price-to-Earnings Ratio: {data[symbol2]['quote']['peRatio']}",
      })

    except:
      return render(request, 'compare.html')


  return render(request, 'compare.html')