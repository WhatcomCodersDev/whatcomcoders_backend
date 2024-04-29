import os
import google
import requests
import collections

collections.Iterable = collections.abc.Iterable

from flask.globals import request
from google.oauth2 import id_token
from googleapiclient.discovery import build


class FlowManager:
    def __init__(self, flow):
        self.flow = flow

    def get_user_info(self, credentials: google.oauth2.credentials.Credentials):
        service = build('people', 'v1', credentials=credentials)
        results = service.people().get(resourceName='people/me', 
                                    personFields='names,emailAddresses,photos').execute()
        
        user_info = {
            "name": results.get("names")[0].get("displayName") if results.get("names") else None,
            "email": results.get("emailAddresses")[0].get("value") if results.get("emailAddresses") else None,
            "picture": results.get("photos")[0].get("url") if results.get("photos") else None
        }

        return user_info

    def get_credentials_from_flow(self):
        self.flow.fetch_token(authorization_response=request.url)
        credentials = self.flow.credentials
        return credentials

    def get_id_info(self, credentials: google.oauth2.credentials.Credentials):
        request_session = requests.session()
        token_request = google.auth.transport.requests.Request(
            session=request_session)

        id_info = id_token.verify_oauth2_token(id_token=credentials._id_token,
                                            request=token_request,
                                            audience=os.getenv('GOOGLE_CLIENT_ID'))
        del id_info["aud"]
        return id_info
    
    def get_flow_authorization_url(self):
        authorization_url, state = self.flow.authorization_url()
        print("authorization_url", authorization_url)
        return authorization_url, state
