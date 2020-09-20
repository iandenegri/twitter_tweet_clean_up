import os
from environs import Env

env = Env()
env.read_env()

consumer_key = os.environ.get('consumer_key') if os.environ.get('consumer_key') else 'TH1SNEED5T0BEREPLAC3D'

consumer_secret = os.environ.get('consumer_secret') if os.environ.get('consumer_secret') else 'TH1SNEED5T0BEREPLAC3D'

access_token_key = os.environ.get('access_token_key') if os.environ.get('access_token_key') else 'TH1SNEED5T0BEREPLAC3D'

access_token_secret = os.environ.get('access_token_secret') if os.environ.get('access_token_secret') else 'TH1SNEED5T0BEREPLAC3D'