import requests
import json

def generate_quote(indx) -> tuple:
    response = requests.get('https://api.forismatic.com/api/1.0/?method=getQuote&format=json')
    if response.status_code == 200:
        jsdata = json.loads(response.text)
        data = (jsdata['quoteText'], jsdata['quoteAuthor'])
        return data[indx]