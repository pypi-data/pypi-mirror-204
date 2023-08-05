import requests
import json

class ConvertAll:
    def __init__(self, headers):
        self.base_url = 'https://currensees.com/v1'
        self.headers = headers

    def convert_all_currencies(self, base_currency, amount, date):
        url = f'{self.base_url}/convert_all'
        data = {
            'base_currency': base_currency,
            'amount': amount,
            'date': date
        }
        response = requests.post(url, headers=self.headers, data=json.dumps(data))
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to convert all currencies: {response.text}")
