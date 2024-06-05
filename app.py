import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify, send_from_directory, request
from selenium_script import get_trending_topics
import threading
import logging

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/run_script')
def run_script():
    result = {}
    use_sample_data = request.args.get('use_sample_data', 'false').lower() == 'true'
    
    def selenium_task():
        nonlocal result
        result = get_trending_topics(use_sample_data=use_sample_data)
        app.logger.info(f"Fetched topics: {result}")
    
    thread = threading.Thread(target=selenium_task)
    thread.start()
    thread.join()
    
    return jsonify(result)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True)
