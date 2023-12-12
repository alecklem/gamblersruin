from flask import Flask, jsonify
from flask_cors import CORS
from nba_api.stats.endpoints import commonallplayers

app = Flask(__name__)
CORS(app) 

@app.route('/loadplayers', methods=['GET'])
def load_players():
    try:
        # Use the nba_api to get all current players
        players_endpoint = commonallplayers.CommonAllPlayers(is_only_current_season=1)
        players_data = players_endpoint.get_json()

        # Extract relevant player information (you may need to adapt this based on the API response structure)
        players = []
        for player in players_data['resultSets'][0]['rowSet']:
            player_info = {
                'id': player['PERSON_ID'],  # Adjust the index based on the actual structure
                'full_name': f"{player['DISPLAY_LAST_COMMA_FIRST']}",
                'team': player['TEAM_ABBREVIATION'],
            }
            players.append(player_info)



        # Return the player data in the response
        return jsonify({'players': players})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
