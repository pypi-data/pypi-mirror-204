import requests
import json

class Historical:
    def __init__(self, headers):
        self.base_url = 'https://currensees.com/v1'
        self.headers = headers

    def get_historical(self, username, date, day, month, year):
        url = f'{self.base_url}/historical'
        params = {
            'username': username,
            'date': date,
            'day': day,
            'month': month,
            'year': year
        }
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get historical data: {response.text}")

    def get_historical_currency(self, uuid, username, day, month, year, date_string):
        url = f'{self.base_url}/historical/{uuid}'
        params = {
            'username': username,
            'day': day,
            'month': month,
            'year': year,
            'date_string': date_string
        }
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get historical currency: {response.text}")