from flask import Flask
from sqlalchemy import create_engine
from controllers.routes import main
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the environment variables
db_name = os.getenv('POSTGRES_DB')
db_user = os.getenv('POSTGRES_USER')
db_pass = os.getenv('POSTGRES_PASSWORD')
db_host = os.getenv('POSTGRES_HOST')
db_port = os.getenv('POSTGRES_PORT')

app = Flask(__name__)
app.register_blueprint(main) # Register the blueprint

# Connect to the database
db_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)
db = create_engine(db_string)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)