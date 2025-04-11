from flask import Flask

# Create a simple Flask app for testing
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello from Page & Brand Business Finder!"

@app.route('/api/test')
def test():
    return {"status": "ok", "message": "API is working"}
