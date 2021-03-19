import pandas as pd
import requests
try:
  from keys import *
except:
  from pro_keys import *
  
# read csv
stocks = pd.read_csv('sp_500_stocks.csv')

# chunk list to make it easier to process
def chunks(lst, n):
  for i in range(0, len(lst), n):
    yield lst[i:i + n]

symbol_groups = list(chunks(stocks['Ticker'], 100))
symbol_strings = []
for i in range(0, len(symbol_groups)):
  symbol_strings.append(','.join(symbol_groups[i]))

rv_columns = [
  'Ticker',
  'Price',
  'P/E Ratio',
  'Price to Book Ratio',
  'Price to Sales Ratio',
  'Percentage Change (1-Month)',
  'Percentage Change (3-Months)',
  'Percentage Change (6-Months)',
  'Percentage Change (1-Year)',
  'Percentage Change (5-Years)',
]

rv_dataframe = pd.DataFrame(columns = rv_columns)

# populate dataframe
for symbol_string in symbol_strings:
  batch_api_call = f'https://sandbox.iexapis.com/stable/stock/market/batch?symbols={symbol_string}&types=quote,stats,advanced-stats&token={CLOUD_API_KEY}'
  data = requests.get(batch_api_call).json()
  for symbol in symbol_string.split(','):
      rv_dataframe = rv_dataframe.append(
      pd.Series(
        [
          symbol,
          data[symbol]['quote']['latestPrice'],
          data[symbol]['quote']['peRatio'],
          data[symbol]['advanced-stats']['priceToBook'],
          data[symbol]['advanced-stats']['priceToSales'],
          data[symbol]['stats']['month1ChangePercent'],
          data[symbol]['stats']['month3ChangePercent'],
          data[symbol]['stats']['month6ChangePercent'],
          data[symbol]['stats']['year1ChangePercent'],          
          data[symbol]['stats']['year5ChangePercent'],
        ],
        index = rv_columns
      ),
      ignore_index = True
    )

# display percentile
times = [
  'Percentage Change (1-Month)',
  'Percentage Change (3-Months)',
  'Percentage Change (6-Months)',
  'Percentage Change (1-Year)',
  'Percentage Change (5-Years)',
]

for time in times:
  rv_dataframe[f'{time}'] = rv_dataframe[f'{time}']*100


# deal with missing data in dataframe
for column in [
  'P/E Ratio', 
  'Price to Book Ratio', 
  'Price to Sales Ratio',
  'Percentage Change (1-Month)',
  'Percentage Change (3-Months)',
  'Percentage Change (6-Months)',
  'Percentage Change (1-Year)',
  'Percentage Change (5-Years)',
  ]:
  rv_dataframe[column].fillna(rv_dataframe[column].mean(), inplace = True)

rv_dataframe[rv_dataframe.isnull().any(axis=1)]

# rounding all values
rounding = [
  'Price',
  'P/E Ratio', 
  'Price to Book Ratio', 
  'Price to Sales Ratio',
  'Percentage Change (1-Month)',
  'Percentage Change (3-Months)',
  'Percentage Change (6-Months)',
  'Percentage Change (1-Year)',
  'Percentage Change (5-Years)',
  ]

for round in rounding:
  rv_dataframe[round] = rv_dataframe[round].round(2)