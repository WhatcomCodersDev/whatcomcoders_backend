import os
import google
import pathlib
import requests
import collections

collections.Iterable = collections.abc.Iterable


from flask.globals import request
from google.oauth2 import id_token
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow

PATH_TO_CLIENT_SECRET = os.path.join(
        pathlib.Path(__file__).parent, "../../client_secret.json")

# https://google-auth.readthedocs.io/en/master/user-guide.html

class GoogleSignInFlowManager:
    ''' Class to manage the flow of the Google OAuth2.0 process.
    '''
    def __init__(self):
        self.flow = self.__setup_google_auth_flow__()

    def __setup_google_auth_flow__(self) -> Flow:
        ''' Setups Google Oauth Flow class.
        https://google-auth-oauthlib.readthedocs.io/en/latest/reference/google_auth_oauthlib.flow.html

            +--------+                               +---------------+
            |        |--(A)- Authorization Request ->|   Resource    |
            |        |                               |     Owner     |
            |        |<-(B)-- Authorization Grant ---|               |
            |        |                               +---------------+
            |        |
            |        |                               +---------------+
            |        |--(C)-- Authorization Grant -->| Authorization |
            | Client |                               |     Server    |
            |        |<-(D)----- Access Token -------|               |
            |        |                               +---------------+
            |        |
            |        |                               +---------------+
            |        |--(E)----- Access Token ------>|    Resource   |
            |        |                               |     Server    |
            |        |<-(F)--- Protected Resource ---|               |
            +--------+                               +---------------+
        
            
        
        '''
    
        flask_env = os.environ.get('FLASK_ENV')
        print(f"FLASK_ENV: {flask_env}")
        if flask_env == 'development':
            redirect_uri = "http://localhost:4000/callback"
        elif flask_env == 'production':
            redirect_uri = "https://gothic-sled-375305.uc.r.appspot.com/callback"
        else:
            raise ValueError(f"Unexpected FLASK_ENV value: {flask_env}")


        flow = Flow.from_client_secrets_file(
            client_secrets_file=PATH_TO_CLIENT_SECRET,
            scopes=[
                "https://www.googleapis.com/auth/userinfo.profile",
                "https://www.googleapis.com/auth/userinfo.email",
                "openid",
            ],
            redirect_uri=redirect_uri
        )
        return flow

    def get_flow_authorization_url(self):
        ''' Get the authorization URL for the Google OAuth2.0 flow.
        
        This is the url you get when you give consent to the app to access your Google account.
        This is step 1 in the OAuth2.0 flow diagram. (A -> B)
        '''
        try:
            authorization_url, state = self.flow.authorization_url(prompt='consent')
            return authorization_url, state
        except Exception as e:
            raise RuntimeError(f"Failed to get authorization URL: {str(e)}")

    def get_credentials_from_flow(self, authorization_response_url: str):
        ''' Get the credentials from the Google OAuth2.0 flow.
        
        This is step 2 in the OAuth2.0 flow diagram. (C -> D)
        '''
        try:
            print(f"authorization_response_url: {authorization_response_url}")
            self.flow.fetch_token(authorization_response=authorization_response_url)
            credentials = self.flow.credentials
            return credentials
        except Exception as e:
            raise RuntimeError(f"Failed to fetch credentials: {str(e)}")

    def get_id_info(self, credentials: google.oauth2.credentials.Credentials):
        ''' Get the ID info from the Google OAuth2.0 flow.'''
        try:
            request_session = requests.session()
            token_request = google.auth.transport.requests.Request(session=request_session)
            id_info = id_token.verify_oauth2_token(
                id_token=credentials._id_token,
                request=token_request,
                audience=os.getenv('GOOGLE_CLIENT_ID')
            )
            del id_info["aud"]
            return id_info
        except Exception as e:
            raise RuntimeError(f"Failed to verify ID token: {str(e)}")  
    
    def get_user_info(self, credentials: google.oauth2.credentials.Credentials):
        ''' Get the user info from the Google OAuth2.0 flow.
        
        We will use the people API to get the user's info.
        '''
        try:
            service = build('people', 'v1', credentials=credentials)
            results = service.people().get(resourceName='people/me', personFields='names,emailAddresses,photos').execute()
            user_info = {
                "name": results.get("names")[0].get("displayName") if results.get("names") else None,
                "email": results.get("emailAddresses")[0].get("value") if results.get("emailAddresses") else None,
                "picture": results.get("photos")[0].get("url") if results.get("photos") else None
            }
            return user_info
        except Exception as e:
            raise RuntimeError(f"Failed to get user info: {str(e)}")


    
