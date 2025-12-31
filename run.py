# run.py
from flask import Flask
from app.routes import init_routes
from dotenv import load_dotenv

load_dotenv() # Load your .env secrets

app = Flask(__name__)

# Initialize the routes
init_routes(app)

if __name__ == '__main__':
    # Listen on Port 9000
    print("Starting server on port 9000...")
    app.run(host='0.0.0.0', port=9000)