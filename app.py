from flask import Flask
from sqlalchemy import create_engine
from controllers.routes import main

app = Flask(__name__)
app.register_blueprint(main) # Register the blueprint

db_name = 'database'
db_user = 'username'
db_pass = 'secret'
db_host = 'db'
db_port = '5432'

# Connect to the database
db_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)
db = create_engine(db_string)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)