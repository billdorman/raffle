import requests
import logging
import os
from config import const as CONSTANTS

from_email = 'Sweeny PTO <donotreply@sweenypto.org>'
message_subject = 'Sweeny PTO - Raffle Information'
message_body = 'Thank you for registering for the Sweeny PTO Raffle. We appreciate the support!'

def send_email(user):

	welcome_html = """\
  Hello!
  
  Thank you for registering for the Sweeny PTO Raffle. We appreciate your support! Please note that 100% of all proceeds go to support the children and teachers of Sweeny Elementrary. 
  
  If you haven't already, you can visit sweenypto.org to enter yourself into drawings for a number of great raffles! Please note that some drawings are for local delivery only while others may be shipped for a small fee.
  
  Please reach out to us with any issues or questions at sweenyelementarypto@gmail.com.

  Regards,
  The Sweeny PTO
"""
	return requests.post(
		CONSTANTS.EMAIL_API_URL,
		auth=("api", CONSTANTS.EMAIL_API_KEY),
		data={"from": from_email,
			"to": user.email,
			"subject": message_subject,
			"text": welcome_html})