from flask import Flask, jsonify, request
import requests
from flask_cors import CORS
from flask_caching import Cache
from nba_api.stats.static import players
from nba_api.stats.endpoints import playerdashboardbygeneralsplits, playerprofilev2
import logging
from datetime import datetime

app = Flask(__name__)
CORS(app)
API_KEY = '69501df68e79bf9926e950a6e58563eb'
BASE_URL = 'https://api.the-odds-api.com/v4/sports'

# Configure caching
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def get_season_by_date(date):
    year = date.year
    if date.month >= 10:  # Season starts in October
        return f"{year}-{str(year + 1)[-2:]}"
    else:  # Season is in the new year but refers to the previous year's start
        return f"{year - 1}-{str(year)[-2:]}"
    
@app.route('/api/odds/')
def get_odds(sport):
    url = f"{BASE_URL}/basketball_nba/odds"
    params = {
        'apiKey': API_KEY,
        'regions': 'us',  
        'markets': 'totals',  # Adjust markets as needed
    }
    response = requests.get(url, params=params)
    data = response.json()
    return jsonify(data)

@app.route('/')
def default():
    return "hello"

@app.route('/loadplayers', methods=['GET'])
@cache.cached(timeout=3600)  # Cache for 1 hour
def load_players():
    try:
        return jsonify(players.get_active_players())
    except Exception as e:
        app.logger.error(f"Error loading players: {e}")
        return jsonify({'error': str(e)}), 500
    
    
@app.route('/points', methods=['POST'])
@cache.cached(timeout=300)  # Cache for 5 minutes
def points():
    try:
        data = request.get_json()
        app.logger.debug(f"Received data: {data}")

        player = data.get('player')
        playerID = player["id"]
        app.logger.debug(f"Player ID: {playerID}")

        current_date = datetime.now()
        season = get_season_by_date(current_date)
        app.logger.debug(f"Using season: {season}")

        player_dashboard = playerdashboardbygeneralsplits.PlayerDashboardByGeneralSplits(player_id=playerID, season=season)
        player_dashboard_data = player_dashboard.get_normalized_dict()
        app.logger.debug(f"Player Dashboard Data: {player_dashboard_data}")

        if not player_dashboard_data["OverallPlayerDashboard"]:
            app.logger.error(f"No data found in OverallPlayerDashboard for season {season}")
            # Try previous season if no data is found for the current season
            previous_season = get_season_by_date(current_date.replace(year=current_date.year - 1))
            app.logger.debug(f"Falling back to previous season: {previous_season}")

            player_dashboard = playerdashboardbygeneralsplits.PlayerDashboardByGeneralSplits(player_id=playerID, season=previous_season)
            player_dashboard_data = player_dashboard.get_normalized_dict()
            app.logger.debug(f"Player Dashboard Data for previous season: {player_dashboard_data}")

            if not player_dashboard_data["OverallPlayerDashboard"]:
                app.logger.error(f"No data found in OverallPlayerDashboard for previous season {previous_season}")
                return jsonify({
                    'error': 'No data found in OverallPlayerDashboard for both current and previous seasons',
                    'points_per_game': None,
                    'player_team_abbreviation': "N/A",
                    'opponent_team_abbreviation': "N/A"
                }), 500

        player_stats = player_dashboard_data["OverallPlayerDashboard"][0]
        app.logger.debug(f"Player Stats: {player_stats}")

        total_points = player_stats["PTS"]
        games_played = player_stats["GP"]
        points_per_game = total_points / games_played if games_played > 0 else 0
        app.logger.debug(f"Points Per Game: {points_per_game}")

        player_profile = playerprofilev2.PlayerProfileV2(player_id=playerID)
        player_profile_data = player_profile.get_normalized_dict()
        app.logger.debug(f"Player Profile Data: {player_profile_data}")

        if not player_profile_data["NextGame"]:
            app.logger.debug("No data found in NextGame")
            return jsonify({
                'points_per_game': points_per_game,
                'player_team_abbreviation': "N/A",
                'opponent_team_abbreviation': "N/A"
            })

        next_game_info = player_profile_data["NextGame"][0]
        app.logger.debug(f"Next Game Info: {next_game_info}")

        player_team_abbreviation = next_game_info["PLAYER_TEAM_ABBREVIATION"]
        opponent_team_abbreviation = next_game_info["VS_TEAM_ABBREVIATION"]

        return jsonify({
            'points_per_game': points_per_game,
            'player_team_abbreviation': player_team_abbreviation,
            'opponent_team_abbreviation': opponent_team_abbreviation
        })

    except Exception as e:
        app.logger.error(f"Error in /points route: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
