from dotenv import load_dotenv
load_dotenv()

import os

spotify = {
    'SPOTIFY_CLIENT_ID': os.getenv('SPOTIFY_CLIENT_ID'),
    'SPOTIFY_CLIENT_SECRET': os.getenv('SPOTIFY_CLIENT_SECRET')
}

static_files = {
    'MEDIA': {
        'FOLDER': os.getenv('MEDIA_FOLDER'),
        'ALLOWED_EXTENSIONS': ['png', 'jpg', 'jpeg']
    }
}