# entrance.py

from resources_loader import ResourcesLoader
from service_helper import ServiceHelper
from flask import Flask, request, jsonify

# Initialize resources loader
resources = ResourcesLoader()

# Initialize Flask application
app = Flask(__name__)

# Initialize the treatment service search helper class
treatment_search = ServiceHelper(resources)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400
    
    results = treatment_search.search(query)
    return jsonify(results)

@app.route('/initialize', methods=['POST'])
def initialize():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Data is required"}), 400
    
    treatment_search.initialize(data)
    return jsonify({"message": "Initialization successful"}), 200

# http://127.0.0.1:5000/search?query=I am from Jefferson County, Alabama and I am feeling very anxious after using cocaine. I don't know what to do. Can you help me? I also have eager to hit someone. I am feeling very aggressive.
@app.route('/client_request', methods=['GET'])
def client_request():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400
    
    results = treatment_search.client_request(query)
    return jsonify(results)


if __name__ == '__main__':
    # For testing purposes, you can load some initial data here
    initial_data = [
        {"name": "Service A", "description": "Description of Service A"},
        {"name": "Service B", "description": "Description of Service B"},
        # Add more initial data as needed
    ]
    
    treatment_search.initialize(initial_data)
    app.run(debug=True)
