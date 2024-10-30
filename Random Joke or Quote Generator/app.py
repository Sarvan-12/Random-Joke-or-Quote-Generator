from flask import Flask, jsonify, request, send_file
import requests

app = Flask(__name__)

# Define the API URLs
joke_api_url = "https://official-joke-api.appspot.com/random_joke"
quote_api_url = "https://zenquotes.io/api/random"

@app.route('/')
def index():
    return send_file('index.html')  # Serve the HTML file directly

@app.route('/style.css')
def send_css():
    return send_file('style.css')  # Serve the CSS file directly

@app.route('/get_quote', methods=['GET'])
def get_quote():
    category = request.args.get('category', 'humor')
    try:
        if category == 'humor':
            # Fetch a random joke from the joke API
            response = requests.get(joke_api_url)
            if response.status_code == 200:
                joke = response.json()
                return jsonify({"quote": f"{joke['setup']} {joke['punchline']} "})
            else:
                return jsonify({"quote": "Failed to fetch a joke"}), 500
        elif category == 'motivation':
            # Fetch a random motivational quote from the quote API
            response = requests.get(quote_api_url)
            if response.status_code == 200:
                quote = response.json()[0]
                return jsonify({"quote": quote['q']})
            else:
                return jsonify({"quote": "Failed to fetch a quote"}), 500
        else:
            return jsonify({"quote": "Category not found"}), 400
    except Exception as e:
        return jsonify({"quote": "An error occurred while fetching data"}), 500

if __name__ == '__main__':
    app.run(debug=True)
    