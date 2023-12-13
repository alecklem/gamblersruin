from flask import Flask, jsonify
from flask_cors import CORS
from nba_api.stats.static import players

app = Flask(__name__)
CORS(app) 

@app.route('/')
def default():
    return "hello"


@app.route('/loadplayers', methods=['GET'])
def load_players():
    try:
        return players.get_active_players()

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
