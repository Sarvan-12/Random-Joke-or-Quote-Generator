from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)

# Define the API URLs
joke_api_url = "https://official-joke-api.appspot.com/random_joke"
quote_api_url = "https://zenquotes.io/api/random"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_quote', methods=['GET'])
def get_quote():
    category = request.args.get('category', 'humor')
    try:
        if category == 'humor':
            res = requests.get(joke_api_url)
            if res.status_code == 200:
                joke = res.json()
                return jsonify({"quote": f"{joke['setup']} {joke['punchline']}"})
            return jsonify({"quote": "Failed to fetch a joke"}), 500

        elif category == 'motivation':
            res = requests.get(quote_api_url)
            if res.status_code == 200:
                q = res.json()[0]
                return jsonify({"quote": f"{q['q']} –{q['a']}"})
            return jsonify({"quote": "Failed to fetch a quote"}), 500

        else:
            return jsonify({"quote": "Unknown category"}), 400

    except Exception:
        return jsonify({"quote": "Error fetching data"}), 500

if __name__ == '__main__':
    app.run(debug=True)