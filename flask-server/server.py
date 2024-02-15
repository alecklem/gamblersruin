from flask import Flask, jsonify, request
from flask_cors import CORS
from nba_api.stats.static import players
from nba_api.stats.endpoints import leaguegamelog, boxscoretraditionalv2, playerdashboardbygeneralsplits, playerprofilev2
from nba_api.stats.static import teams


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
        playerID = (player["id"])
        player_dashboard = playerdashboardbygeneralsplits.PlayerDashboardByGeneralSplits(player_id=playerID, season="2023-24")
        player_stats = player_dashboard.get_normalized_dict()["OverallPlayerDashboard"][0]
        #1
        # Player points per game for season
        total_points = player_stats["PTS"]
        games_played = player_stats["GP"]
        points_per_game = total_points / games_played if games_played > 0 else 0

        print(f"Player Points Per Game: {points_per_game}")

        #2 
        # Last 5 games performance
        # Get home team ID and away team ID for future stats
        player_profile = playerprofilev2.PlayerProfileV2(player_id=playerID)
        next_game_info = player_profile.get_normalized_dict()["NextGame"][0]
        # Extract player team abbreviation
        player_team_abbreviation = next_game_info["PLAYER_TEAM_ABBREVIATION"]
        print(f"Team Abbreviation: {player_team_abbreviation}")
        # Extract opponent team abbreviation
        opponent_team_abbreviation = next_game_info["VS_TEAM_ABBREVIATION"]
        print(f"Opponent Team Abbreviation: {opponent_team_abbreviation}")
        # Extract next game details
        print(f"Next Game Info: {next_game_info}")

        #3 Get the last 5 games for the player
        game_log = leaguegamelog.LeagueGameLog(season="2023-24", direction="DESC", date_from_nullable="2023-08-01", season_type_all_star="Regular Season", player_or_team_abbreviation="T", counter=200)
        all_games = game_log.get_normalized_dict()["LeagueGameLog"]
        # Filter games for a specific team and player
        team_games = [game for game in all_games if game['TEAM_ABBREVIATION'] == player_team_abbreviation]
        specific_player_games = []
        for game in team_games:
            game_id = game['GAME_ID']
            box_score = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id)
            player_stats = box_score.get_normalized_dict()["PlayerStats"]
            for stat in player_stats:
                if stat["PLAYER_ID"] == playerID and (float(stat["MIN"].split(':')[0])) > 0:
                    specific_player_games.append(game)
        last_5_player_games = specific_player_games[:5]
        # Extract player points using box scores
        player_points_in_last_5_games = []
        for game in last_5_player_games:
            game_id = game['GAME_ID']
            box_score = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id)
            player_stats = box_score.get_normalized_dict()["PlayerStats"]
            player_points = next((stat["PTS"] for stat in player_stats if stat["PLAYER_ID"] == playerID), 0)
            player_points_in_last_5_games.append(player_points)

        #4 Player performance against opponent team
        games_against_opponent = [game for game in specific_player_games if game['MATCHUP'][-3:] == opponent_team_abbreviation]
        # Extract player points in games against the opposing team
        player_points_against_opponent = []
        for game in games_against_opponent:
            game_id = game['GAME_ID']
            box_score = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id)
            player_stats = box_score.get_normalized_dict()["PlayerStats"]
            player_points = next((stat["PTS"] for stat in player_stats if stat["PLAYER_ID"] == playerID), 0)
            player_points_against_opponent.append(player_points)


        print(player_points_against_opponent)
        print(f"Player Points in Last 5 Games: {player_points_in_last_5_games}")

        return jsonify({'team_abbreviation': player_team_abbreviation, 'opponent_team_abbreviation': opponent_team_abbreviation, 'points_per_game': points_per_game, 'player_points_in_last_5_games': player_points_in_last_5_games, 'player_points_against_opponent': player_points_against_opponent})


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
