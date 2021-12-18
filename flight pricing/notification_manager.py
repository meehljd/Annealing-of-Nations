from twilio.rest import Client
import os

SID = os.environ['TWILIO_SID']
TOKEN = os.environ['TWILIO_TOKEN']
TO_PHONE = os.environ['MY_PHONE']
FROM_PHONE = os.environ['TWILIO_PHONE']


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.client = Client(SID, TOKEN)

    def send_sms(self, alert_message):
        message = self.client.messages.create(
            body=alert_message,
            from_=FROM_PHONE,
            to=TO_PHONE
        )
        # Prints if successfully sent.
        print(message.sid)
