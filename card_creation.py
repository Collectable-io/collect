# Sandbox Implementation
# Todo: 
# Add functionality to enroll account via plaid - https://docs.lithic.com/reference/post_fundingsource-plaid
# Verify authorization of virtual card works - https://docs.lithic.com/reference/post_simulate-authorize
# Verify virtual card is capable of clearing a transaction - https://docs.lithic.com/reference/post_simulate-clearing
# Add voiding a transaction functionality - https://docs.lithic.com/reference/post_simulate-void

import requests
from datetime import date
import json

url_card_creation = "https://sandbox.lithic.com/v1/card"
url_bank_funding = "https://sandbox.lithic.com/v1/fundingsource/bank"
url_bank_validation = "https://sandbox.lithic.com/v1/fundingsource/bank/validate"
url_card_refund = "https://sandbox.lithic.com/v1/simulate/return"

today = date.today()
month = today.strftime("%m")
year = today.strftime("%Y")

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": "api-key 9470a0ba-c929-417a-927e-0756678b41de"
}


class funding_card:
    def __init__(self, account_number, routing_number):
        self.account_number = account_number
        self.routing_number = routing_number
        self.funding_card_dict = {}
        self.funding_card_validation_dict = {}
        self.funding_card_token = ""

    def initiate_funding_card(self):
        payload = {
            "account_number": self.account_number,
            "routing_number": self.routing_number
        }
        self.funding_card_dict = requests.request("POST", url_bank_funding, json=payload, headers=headers).json()
        self.funding_card_token = self.funding_card_dict['data']['token']

    def validate_funding_card(self):
        payload = {
            "micro_deposits": [2, 3, 5],
            "token": self.funding_card_token
        }
        self.funding_card_validation_dict = requests.request("POST", url_bank_validation, json=payload, headers=headers).json()


class virtual_card:
    def __init__(self, use, spending_limit, funding_token):
        self.memo = use
        self.amount = spending_limit
        self.funding_token = funding_token
        self.virtual_card_dict = {}
        self.virtual_card_refund_dict = {}
        self.virtual_card_token = ""
        self.virtual_card_pan = ""
        self.virtual_card_cvv = ""
        self.virtual_card_exp_month = ""
        self.virtual_card_exp_year = ""

    def initiate_virtual_card(self):
        payload = {
            "type": "SINGLE_USE", # Or DIGITAL_WALLET
            "exp_month": month,
            "exp_year": year,
            "funding_token": self.funding_token,
            "memo": self.memo,
            "spend_limit": self.amount,
            "spend_limit_duration": "TRANSACTION",
            "state": "PAUSED" # Switch to "OPEN" upon funding: Card will approve authorizations (if they match card and account parameters)
        }
        self.virtual_card_dict = requests.request("POST", url_card_creation, json=payload, headers=headers).json()
        self.virtual_card_token = self.virtual_card_dict['token']
        self.virtual_card_pan = self.virtual_card_dict['pan']
        self.virtual_card_cvv = self.virtual_card_dict['cvv']
        self.virtual_card_exp_month = self.virtual_card_dict['exp_month']
        self.virtual_card_exp_year = self.virtual_card_dict['exp_year']

    def open_virtual_card(self):
        self.virtual_card_dict["state"] = "OPEN"

    def refund_virtual_card(self):
        payload = {
            "amount": self.amount,
            "descriptor": self.memo,
            "pan": self.virtual_card_pan
        }
        self.virtual_card_refund_dict = requests.request("POST", url_card_refund, json=payload, headers=headers).json()

    
