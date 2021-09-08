import requests
from twilio.rest import Client

#Add the company symbol
STOCK = "TSLA"

#Add the company name to get the news articles
COMPANY_NAME = "Tesla"

#API to get the stock information
URL = "https://www.alphavantage.co/query"

#Get a unique API key from Alpha Vantage
STOCK_API_KEY = "ZM6LUUAG0K1DWG39"

#Get a unique API key from NewsApi
NEWS_API_KEY = "3d15742d082f4f3f8c0b0baa629589db"

#Get a unique Account_SID from Twilio
ACCOUNT_SID = "AC44da8db19ff2f3f344df16dfe22beb09"

#Get a unique Auth_Token from Twilio
AUTH_TOKEN = "72916990d537f3356cefa394c567be26"

#Add your Twilio account SMS number. Use the format "+" and then the full phone number including country code with no dashes or paranthesis (Example: +15555555555).
TWILIO_NUMBER = "+19794818786"

#Add your phone number. Use the format "+" and then the full phone number including country code with no dashes or paranthesis (Example: +15555555555)
INVESTOR_NUMBER = "+18575236065"

parameters = {
    'function': "TIME_SERIES_DAILY",
    'symbol': STOCK,
    'outputsize': 'compact',
    'apikey': STOCK_API_KEY
}

response = requests.get(URL, params=parameters)
response.raise_for_status()
stock_data = response.json()
stock_data_list = [values for key,values in stock_data['Time Series (Daily)'].items()]
stock_price_1 = float(stock_data_list[0]['4. close'])
stock_price_2 = float(stock_data_list[1]['4. close'])

YESTERDAY = stock_data['Meta Data']['3. Last Refreshed']

news_params = {
    "q": COMPANY_NAME,
    "from": YESTERDAY,
    "language": "en",
    "sortBy": "publishedAt",
    "apiKey": NEWS_API_KEY,
}
news_response = requests.get(url="https://newsapi.org/v2/everything",params=news_params)
news_response.raise_for_status()
news_data = news_response.json()

articles = news_data['articles']
articles_list = articles[0:3]

percent_change = round(((stock_price_1/stock_price_2) - 1) * 100,2)

up_down_arrow = ""
if percent_change > 0:
    up_down_arrow = f"🔺"

elif percent_change < 0:
    up_down_arrow = f"🔻"

for article in articles_list:
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages \
                .create(
                    body=f"\n{STOCK}: {up_down_arrow}{abs(percent_change)}% \n Headline: {article['title']} \n Brief: {article['description']}",
                    from_=TWILIO_NUMBER,
                    to=INVESTOR_NUMBER
    )