import datetime
import os

# Server Name
SERVER_NAME = "RAFFLE_SERVER_01"

BASE_URL = "https://sweenypto.org"

# Email Config - Mailgun

EMAIL_API_URL = os.environ.get('EMAIL_API_URL')
EMAIL_API_KEY = os.environ.get('EMAIL_API_KEY')

# Database
DB_ENGINE = 'mysql+pymysql'

DB_SERVER = os.environ.get('RAFFLE_DB_SERVER')
DB_USER = os.environ.get('RAFFLE_DB_USER')
DB_PASS = os.environ.get('RAFFLE_DB_PASS')
DB_SCHEMA = os.environ.get('RAFFLE_DB_SCHEMA')

DB_CONNECTION_STRING = '{engine}://{user}:{password}@{server}/{schema}'.format(
    engine=DB_ENGINE, user=DB_USER, password=DB_PASS, server=DB_SERVER, schema=DB_SCHEMA)

# JWT TOKENS
JWT_SECRET = 'a121dfa5-bf7b-4d61-8383-d78ffce36e14'
SECRET = 'fd7f4f00-b921-4ad6-af96-5798d7404667'
JWT_ACCESS_TOKEN_EXPIRATION = datetime.timedelta(hours=1)


# Location API
GEO_API = 'http://ip-api.com/json/'

# The max number of threads to spawn for running scheduled tasks
THREAD_LIMIT = 10

# The interval used to run jobs (in seconds)
JOB_INTERVAL = 60

# The interval used to run scheduled jobs (in seconds)
SCHEDULED_JOB_INTERVAL = 60

# Logging Consts

LOG_FILE_NAME = os.environ.get('LOG_FILE_NAME')
LOGGING_LEVEL = 'DEBUG'

STATE_ABBREVIATIONS = ['NA', 'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VI', 'VA', 'WA', 'WV', 'WI', 'WY']


# Square Payment Processing Variables
SQUARE_APP_ID = os.environ.get('RAFFLE_SQUARE_APP_ID')
SQUARE_APP_TOKEN = os.environ.get('RAFFLE_SQUARE_APP_TOKEN')
SQUARE_LOCATION_ID = os.environ.get('RAFFLE_SQUARE_LOCATION_ID')
SQUARE_ACCESS_TOKEN = os.environ.get('RAFFLE_SQUARE_ACCESS_TOKEN')
