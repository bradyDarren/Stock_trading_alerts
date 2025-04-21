import requests
import os
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_URL = 'https://www.alphavantage.co/query?'
NEWS_URL = 'https://newsapi.org/v2/everything?'
AUTH_TOKEN = os.environ.get('TWILIO_TOKEN')
ACCOUNT_SID = os.environ.get('TWILIO_SID')
PHONE_NUMBER = os.environ.get('PNUM')
WHATS_NUMBER = os.environ.get('WNUM')
S_KEY = os.environ.get('STOCK_KEY')
N_KEY = os.environ.get('NEWS_KEY')

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
stock_params = {
    'function':'TIME_SERIES_DAILY',
    'symbol':STOCK,
    'apikey':S_KEY
}
r = requests.get(url=STOCK_URL, params=stock_params)
data = r.json()['Time Series (Daily)']

data_list = [value for _, value in data.items()]

yesterdays_close_price = data_list[0]['4. close']
day_b4_yesterday_close_price = data_list[1]['4. close']

per_change = (float(yesterdays_close_price) - float(day_b4_yesterday_close_price))/float(yesterdays_close_price)

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
news_params = {
    'q':'Tesla',
    'from':'2025-04-17',
    'sortBy':'popularity',
    'apiKey':N_KEY
}
response = requests.get(NEWS_URL,params=news_params)
news = response.json()
print(news)


# STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 
if per_change >= .05 or per_change <= -.05:
    message_body = f"{STOCK} {'🔺' if per_change > 0 else '🔻'} {per_change:.2%}\n"
    for a in range(3):
        message_body += f'Headline: {news['articles'][a]['title']}\n'\
            f'Brief: {news['articles'][a]['description']}\n'

    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages.create(
        body = message_body,    
        from_ = f'whatsapp:{WHATS_NUMBER}',
        to = f'whatsapp:{PHONE_NUMBER}',
    )
    print(message.status)

#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

