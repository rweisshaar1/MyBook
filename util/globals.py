import os
from flask import session
from dotenv import load_dotenv

# Get the absolute path to the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to the .env file
env_path = os.path.join(script_dir, '..', '.env')

# Load environment variables
load_dotenv(env_path)

api_key = os.getenv('GOOGLE_API_KEY')

def Truncate_String(string, length):
    return (string[:length] + '...') if len(string) > length else string