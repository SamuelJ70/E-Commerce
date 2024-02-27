# requests are used to make http request to an url

# import requests

# r = requests.get("https://www.freecodecamp.org/")

# print(r.status_code)

# print(r)


"""
we are using 2 api to get the adress of the user as well as the venodr

1. ipify - this api helps us to know the ip adress from where the request is coming from
2. ipapi - this api helps us to know the location information for a particular ip address 

"""


# Account sid : AC53325f36cc1159ce8d450786f20300d4
# auth token : facc85959cd7690f486d275ce7373719

# phone number : +18585332596


# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client

# Set environment variables for your credentials
# Read more at http://twil.io/secure
account_sid = "AC53325f36cc1159ce8d450786f20300d4"
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)

message = client.messages.create(
    body="hello motherFather", from_="+18585332596", to="+917204946893"
)

print(message.sid)