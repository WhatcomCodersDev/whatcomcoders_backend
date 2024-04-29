import sendgrid
import os
from dotenv import load_dotenv

load_dotenv()

sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
data = {
  "personalizations": [
    {
      "to": [
        {
          "email": os.environ.get('TEST_RECEIVER_EMAIL')
        }
      ],
      "subject": "Sending with SendGrid is Fun"
    }
  ],
  "from": {
    "email": os.environ.get('SENDER_EMAIL')
  },
  "content": [
    {
      "type": "text/plain",
      "value": "Hey Juan, \n \n This email was sent by using the SendGrid API. I am using Cloudflare to redirect this custom email through our domain. Send me an email or message when you have time to get set up. I have this almost set up. \n\n\n Thank you,\n Hansel"
    }
  ]
} 
response = sg.client.mail.send.post(request_body=data)
print(response.status_code)
print(response.body)
print(response.headers)