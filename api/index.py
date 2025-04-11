from flask import Flask, request
import sys
import os

# Add the root directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import your app
from app import app

# This is required for Vercel serverless functions
if __name__ == "__main__":
    app.run()
