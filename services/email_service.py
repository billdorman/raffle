import logging
import os
from config import const as CONSTANTS

from_email = 'Sweeny PTO <donotreply@sweenypto.org>'
message_subject = 'Sweeny PTO - Raffle Information'

def send_email(to_email, message_subject, message_body, from_email):
	return requests.post(
		EMAIL_API_URL,
		auth=("api", EMAIL_API_KEY),
		data={"from": from_email,
			"to": [to_email],
			"subject": message_subject,
			"text": message_body})