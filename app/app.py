from flask import Flask
from prometheus_client import Counter, generate_latest

app = Flask(__name__)

# Define a metric to track request counts
REQUEST_COUNT = Counter('app_request_count', 'Total number of requests')

@app.route('/')
def hello():
    REQUEST_COUNT.inc() # Increment the counter
    return "Hello! I am running on Kubernetes! 🚀"

@app.route('/metrics')
def metrics():
    # Expose metrics for Prometheus to scrape
    return generate_latest()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
