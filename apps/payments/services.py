import requests
import json
import hmac
import hashlib
from django.conf import settings
from decouple import config

class NowPaymentsService:
    API_URL = 'https://api.nowpayments.io/v1'

    def __init__(self):
        self.api_key = config('NOWPAYMENTS_API_KEY', default='')
        self.ipn_secret = config('NOWPAYMENTS_IPN_SECRET', default='')

    def create_invoice(self, order_id, price_amount, price_currency, ipn_callback_url, success_url, cancel_url):
        headers = {
            'x-api-key': self.api_key,
            'Content-Type': 'application/json'
        }
        data = {
            'price_amount': float(price_amount),
            'price_currency': price_currency,
            'order_id': str(order_id),
            'ipn_callback_url': ipn_callback_url,
            'success_url': success_url,
            'cancel_url': cancel_url
        }
        
        try:
            response = requests.post(f'{self.API_URL}/invoice', headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error creating invoice: {e}")
            return None

    def verify_signature(self, request_data, signature):
        sorted_data = json.dumps(request_data, separators=(',', ':'), sort_keys=True)
        digest = hmac.new(
            str(self.ipn_secret).encode(),
            sorted_data.encode(),
            hashlib.sha512
        )
        calculated_signature = digest.hexdigest()
        return calculated_signature == signature
