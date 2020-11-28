import requests
import logging
import os
from config import const as CONSTANTS

from_email = 'Sweeny PTO <donotreply@sweenypto.org>'
message_subject = 'Sweeny PTO - Raffle Information'
message_body = 'Thank you for registering for the Sweeny PTO Raffle. We appreciate the support!'

def send_email(user):
	
	send_email_body=open('templates/welcome-email.html', 'r')
    
	return requests.post(
		CONSTANTS.EMAIL_API_URL,
		auth=("api", CONSTANTS.EMAIL_API_KEY),
		data={"from": from_email,
			"to": user.email,
			"subject": message_subject,
			"html": send_email_body})

def send_email_reg(user):
	new_user =(f'{user.first_name} {user.last_name}, {user.city}, {user.state} has registered on the Raffle site.')
	return requests.post(
		CONSTANTS.EMAIL_API_URL,
		auth=("api", CONSTANTS.EMAIL_API_KEY),
		data={"from": from_email,
			"to": CONSTANTS.NEW_USER_NOTIFY_EMAIL,
			"subject": "A new user has registered for the Raffle!.",
			"text": new_user})
