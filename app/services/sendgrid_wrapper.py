import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail



import sendgrid
import os
from dotenv import load_dotenv

load_dotenv()


class SendGridWrapper:
    def __init__(self):
        self.sg_api = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))

    def send_email_intro(self, requester_data, receiver_data):
        data = {
            "personalizations": [
                {
                    "to": [
                        {
                        "email": f"{receiver_data['email']}"
                        }
                    ],
                    "subject": f"intro: {requester_data['name']} <> {receiver_data['name']}"
                }

                ],
                 "from": {
                "email": os.environ.get('SENDER_EMAIL'),  # Use a verified sender email address
                },
                "reply_to": {
                    "email": requester_data['email']  # Optional: Add requester's email as reply-to
                },

                "content": [
                    {
                    "type": "text/plain",
                    "value": f"Hey {receiver_data['name']}, \n \n Meet {requester_data['name']} from {requester_data['company']}. They've expressed interest in meeting you based on your profile on Whatcom Coders. \n\n\n Please connect directly, and feel free to remove me from the cc line,\n Hansel"
                    }
                ]
            } 
        print("email data:", data)
        response = self.sg_api.client.mail.send.post(request_body=data)
        return response.status_code

    def send_dummy_mail(self):
        message = Mail(
           from_email=os.environ.get('SENDER_EMAIL'),
            to_emails='to@example.com',
            subject='Sending with Twilio SendGrid is Fun',
            html_content='<strong>and easy to do anywhere, even with Python</strong>')
        try:
            response = self.sg_api.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e) 


            