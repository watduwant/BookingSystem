import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure

account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

def sendmsg(phone, body):
    print(str(phone))
    message = client.messages.create(
                                body=body,
                                from_='+18456227152',
                                to='+91'+phone
                            )

    print(message.sid)