from flask import Flask
from dotenv import load_dotenv
import os
from flask_login import LoginManager
from db.database import db
from models.user import User

# Load environment variables from .env file
load_dotenv()

# Get the environment variables
db_name = os.getenv('POSTGRES_DB')
db_user = os.getenv('POSTGRES_USER')
db_pass = os.getenv('POSTGRES_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('POSTGRES_PORT')
secret_key = os.getenv('SECRET_KEY')

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)

    # Set the secret key
    app.config['SECRET_KEY'] = secret_key
    
    # Initialize LoginManager with the app instance
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    db.init_app(app)

    with app.app_context():
        from controllers.routes import main
        app.register_blueprint(main)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8000)