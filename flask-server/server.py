from flask import Flask, jsonify, request
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
    
@app.route('/points', methods=['POST'])
def points():
    try:
        data = request.get_json()
        player = data.get('player')
        category = data.get('category')

        # Access the player and category data as needed
        player_full_name = player.get('full_name')

        # Perform actions based on player and category data
        result = f"Player: {player_full_name}, Category: {category}"
        print(result)
        return jsonify({'result': result})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/rebounds', methods=['POST'])
def rebounds():
    try:
        data = request.get_json()
        player = data.get('player')
        category = data.get('category')

        # Access the player and category data as needed
        player_full_name = player.get('full_name')

        # Perform actions based on player and category data
        result = f"Player: {player_full_name}, Category: {category}"
        return jsonify({'result': result})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route for handling the 'ASSISTS' category
@app.route('/assists', methods=['POST'])
def assists():
    try:
        data = request.get_json()
        player = data.get('player')
        category = data.get('category')

        # Access the player and category data as needed
        player_full_name = player.get('full_name')

        # Perform actions based on player and category data
        result = f"Player: {player_full_name}, Category: {category}"
        return jsonify({'result': result})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route for handling the '3PT' category
@app.route('/three_pointers', methods=['POST'])
def three_pointers():
    try:
        data = request.get_json()
        player = data.get('player')
        category = data.get('category')

        # Access the player and category data as needed
        player_full_name = player.get('full_name')

        # Perform actions based on player and category data
        result = f"Player: {player_full_name}, Category: {category}"
        return jsonify({'result': result})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/three_point_attempts', methods=['POST'])
def three_point_attempts():
    try:
        data = request.get_json()
        player = data.get('player')
        category = data.get('category')

        # Access the player and category data as needed
        player_full_name = player.get('full_name')

        # Perform actions based on player and category data
        result = f"Player: {player_full_name}, Category: {category}"
        return jsonify({'result': result})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route for handling the 'FG' category
@app.route('/field_goals', methods=['POST'])
def field_goals():
    try:
        data = request.get_json()
        player = data.get('player')
        category = data.get('category')

        # Access the player and category data as needed
        player_full_name = player.get('full_name')

        # Perform actions based on player and category data
        result = f"Player: {player_full_name}, Category: {category}"
        return jsonify({'result': result})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/field_goals_attempted', methods=['POST'])
def field_goals_attempted():
    try:
        data = request.get_json()
        player = data.get('player')
        category = data.get('category')

        # Access the player and category data as needed
        player_full_name = player.get('full_name')

        # Perform actions based on player and category data
        result = f"Player: {player_full_name}, Category: {category}"
        return jsonify({'result': result})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route for handling the 'STEALS' category
@app.route('/steals', methods=['POST'])
def steals():
    try:
        data = request.get_json()
        player = data.get('player')
        category = data.get('category')

        # Access the player and category data as needed
        player_full_name = player.get('full_name')

        # Perform actions based on player and category data
        result = f"Player: {player_full_name}, Category: {category}"
        return jsonify({'result': result})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route for handling the 'BLOCKS' category
@app.route('/blocks', methods=['POST'])
def blocks():
    try:
        data = request.get_json()
        player = data.get('player')
        category = data.get('category')

        # Access the player and category data as needed
        player_full_name = player.get('full_name')

        # Perform actions based on player and category data
        result = f"Player: {player_full_name}, Category: {category}"
        return jsonify({'result': result})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route for handling the 'STOCKS' category
@app.route('/stocks', methods=['POST'])
def stocks():
    try:
        data = request.get_json()
        player = data.get('player')
        category = data.get('category')

        # Access the player and category data as needed
        player_full_name = player.get('full_name')

        # Perform actions based on player and category data
        result = f"Player: {player_full_name}, Category: {category}"
        return jsonify({'result': result})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Route for handling the 'PRA' category
@app.route('/pra', methods=['POST'])
def pra():
    try:
        data = request.get_json()
        player = data.get('player')
        category = data.get('category')

        # Access the player and category data as needed
        player_full_name = player.get('full_name')

        # Perform actions based on player and category data
        result = f"Player: {player_full_name}, Category: {category}"
        return jsonify({'result': result})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route for handling the 'PTS + REBOUNDS' category
@app.route('/points_plus_rebounds', methods=['POST'])
def points_plus_rebounds():
    try:
        data = request.get_json()
        player = data.get('player')
        category = data.get('category')

        # Access the player and category data as needed
        player_full_name = player.get('full_name')

        # Perform actions based on player and category data
        result = f"Player: {player_full_name}, Category: {category}"
        return jsonify({'result': result})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route for handling the 'POINTS + ASSISTS' category
@app.route('/points_plus_assists', methods=['POST'])
def points_plus_assists():
    try:
        data = request.get_json()
        player = data.get('player')
        category = data.get('category')

        # Access the player and category data as needed
        player_full_name = player.get('full_name')

        # Perform actions based on player and category data
        result = f"Player: {player_full_name}, Category: {category}"
        return jsonify({'result': result})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route for handling the 'TURNOVERS' category
@app.route('/turnovers', methods=['POST'])
def turnovers():
    try:
        data = request.get_json()
        player = data.get('player')
        category = data.get('category')

        # Access the player and category data as needed
        player_full_name = player.get('full_name')

        # Perform actions based on player and category data
        result = f"Player: {player_full_name}, Category: {category}"
        return jsonify({'result': result})

    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)
