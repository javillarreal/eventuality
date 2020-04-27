from dotenv import load_dotenv
load_dotenv()

import os

auth0 = {
    'AUTH0_DOMAIN': os.getenv('AUTH0_DOMAIN'),
    'API_AUDIENCE': os.getenv('API_AUDIENCE'),
    'ALGORITHMS': os.getenv('ALGORITHMS').split(' ')
}
