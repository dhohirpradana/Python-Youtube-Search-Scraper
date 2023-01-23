import os
from sys import stderr

from flask import Flask, jsonify, request
from flask_cors import CORS

from yt_scraper_sroll import handler as yt_scraper_sroll_handler

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def hello_geek():
    return '<h1>Hello from Flask</h2>'

@app.route('/youtube_scraper_scroll', methods=['POST'])
def youtube_scraper_scroll():
    return yt_scraper_sroll_handler(request, jsonify)

if __name__ == "__main__":
    app.run(debug=True)