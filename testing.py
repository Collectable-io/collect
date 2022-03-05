from card_creation import funding_card
from card_creation import virtual_card

# Sample funding source parameters
account_number = "1234567"
routing_number = "623852453"

# Initiating funding card
personal_card = funding_card(account_number, routing_number) 
personal_card.initiate_funding_card()
print(personal_card.funding_card_dict)

# Validating funding card
personal_card.validate_funding_card()
print(personal_card.funding_card_validation_dict)

# Sample virtual card addatives 
use = "Rent"
spending_limit = 1000

# Creating virtual card
group_card = virtual_card(use, spending_limit, personal_card.funding_card_token)
group_card.initiate_virtual_card()
print(group_card.virtual_card_dict)

# Making virtual card usable
group_card.open_virtual_card()
print(group_card.virtual_card_dict)