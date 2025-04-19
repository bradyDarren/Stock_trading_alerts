import requests
import datetime

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={STOCK}&apikey='
r = requests.get(url)
data = r.json()

# Obtain the dates for the 1 day from now and 2 days from now.
today = datetime.date.today()
yesterday = str('2025-04-17') # - testing lines
day_b4_yesterday = str('2025-04-16') # - testing lines
# yesterday = str(today - datetime.timedelta(days=1))
# day_b4_yesterday = str(today - datetime.timedelta(days=2))


# yesterdays_close = float(data['Time Series (Daily)'][yesterday]['4. close'])
yesterdays_close = 200 # - testing lines
day_b4_yesterday_close = float(data['Time Series (Daily)'][day_b4_yesterday]['4. close'])

per_change = (yesterdays_close - day_b4_yesterday_close)/yesterdays_close

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
url_1 = (f'https://newsapi.org/v2/everything?'
       'q=Tesla&'
       'from=2025-04-17&'
       'sortBy=popularity&'
       'apiKey=')

response = requests.get(url_1)
news = response.json()
print(news)

if per_change >= .05 or per_change <= -.05:
    if per_change > .00: 
        for a in range(3):
            print(f'{STOCK}🔺{per_change}'
                  f'Healine: {news['articles'][a]['title']}\n'
                  f'Breif: {news['articles'][a]['description']}')
    else: 
         for a in range(3):
            print(f'{STOCK}🔻{per_change}'
                  f'Healine: {news['articles'][a]['title']}\n'
                  f'Breif: {news['articles'][a]['description']}')
## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


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

