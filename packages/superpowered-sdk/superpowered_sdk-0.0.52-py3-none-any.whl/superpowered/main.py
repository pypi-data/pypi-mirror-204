import requests
import base64
import os

# initialize variables
BASE_URL = 'https://api.superpowered.ai/v1/'

def init(api_key_id: str, api_key_secret: str, verbose: bool = False):
    """
    init is used to set the API key for the SDK. It should be called before any other SDK functions are called.
    """
    token = base64.b64encode((f'{api_key_id}:{api_key_secret}').encode('utf-8')).decode('utf-8')
    os.environ['SUPERPOWERED_API_KEY'] = token

def get_headers():
    if 'SUPERPOWERED_API_KEY' not in os.environ:
        # initialize API key
        try:
            api_key_id = os.getenv("SUPERPOWERED_API_KEY_ID")
            api_key_secret = os.getenv("SUPERPOWERED_API_KEY_SECRET")
            init(api_key_id=api_key_id, api_key_secret=api_key_secret)
        except:
            raise NoApiKeyError()
    
    token = os.environ['SUPERPOWERED_API_KEY']
    HEADERS = {'Authorization': f'Bearer {token}'}
    return HEADERS

# exceptions
class NoApiKeyError(Exception):
    def __init__(self):
        super().__init__('Could not find API key ID and secret. Please check that you have the following environment variables set: SUPERPOWERED_API_KEY_ID, SUPERPOWERED_API_KEY_SECRET.')

def _format_http_response(resp: requests.Response):
    if resp.status_code != 200:
        if resp.status_code == 204:
            return {
                'http_code': resp.status_code,
                'body': None
            }
        else:
            #print ("Error:", resp.status_code)
            raise Exception(resp.status_code, resp.json())
    return {
        'http_code': resp.status_code,
        'body': resp.json()
    }