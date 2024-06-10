from flask import Flask, jsonify, request
import requests
from flask_cors import CORS
from flask_caching import Cache
from nba_api.stats.static import players
from nba_api.stats.endpoints import playerdashboardbygeneralsplits, playergamelog, leaguegamelog
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

# Hardcoded date and season for development
HARD_CODED_DATE = datetime(2024, 2, 15)  # Mid-February 2024
HARD_CODED_SEASON = '2023-24'

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

        player = data.get('player')
        playerID = player["id"]
        player_name = player["full_name"]

        # Use hardcoded season and date
        season = HARD_CODED_SEASON
        current_date = HARD_CODED_DATE

        # Fetch player dashboard
        player_dashboard = playerdashboardbygeneralsplits.PlayerDashboardByGeneralSplits(player_id=playerID, season=season)
        player_dashboard_data = player_dashboard.get_normalized_dict()

        # Fetch player game logs for recent performance
        game_logs = playergamelog.PlayerGameLog(player_id=playerID, season=season)
        game_logs_data = game_logs.get_normalized_dict()

        if not player_dashboard_data["OverallPlayerDashboard"]:
            return jsonify({
                'error': 'No data found in OverallPlayerDashboard for current season',
                'points_per_game': None,
                'recent_performance': None,
                'player_team_abbreviation': "N/A",
                'opponent_team_abbreviation': "N/A"
            }), 500

        player_stats = player_dashboard_data["OverallPlayerDashboard"][0]

        total_points = player_stats["PTS"]
        games_played = player_stats["GP"]
        points_per_game = total_points / games_played if games_played > 0 else 0

        # Calculate recent performance (last 5 games)
        recent_games = game_logs_data['PlayerGameLog'][:5]
        recent_points = [game['PTS'] for game in recent_games]

        recent_performance = {
            'games': [game['GAME_DATE'] for game in recent_games],
            'points': recent_points
        }

        # Determine the next game based on the hardcoded date
        league_log = leaguegamelog.LeagueGameLog(season=HARD_CODED_SEASON).get_normalized_dict()

        next_game = None
        for game in league_log['LeagueGameLog']:
            game_date = datetime.strptime(game['GAME_DATE'], "%Y-%m-%d")
            if game_date > current_date:
                next_game = game
                break

        if not next_game:
            return jsonify({
                'points_per_game': points_per_game,
                'recent_performance': recent_performance,
                'player_team_abbreviation': "N/A",
                'opponent_team_abbreviation': "N/A"
            })

        player_team_abbreviation = next_game["TEAM_ABBREVIATION"]
        opponent_team_abbreviation = next_game["MATCHUP"].split()[-1]

        # Matchup History
        matchup_points = []
        for game in league_log['LeagueGameLog']:
            if game['TEAM_ABBREVIATION'] == player_team_abbreviation and game['MATCHUP'].endswith(opponent_team_abbreviation):
                if game['PLAYER_ID'] == playerID:  # Correct field name to access the player ID
                    matchup_points.append({
                        'game_date': game['GAME_DATE'],
                        'points': game['PTS']
                    })

        # Home vs Away Performance
        home_games = []
        away_games = []
        for game in game_logs_data['PlayerGameLog']:
            if game['MIN'] >= 2:
                if game['MATCHUP'].startswith('@'):
                    away_games.append(game['PTS'])
                else:
                    home_games.append(game['PTS'])

        home_avg = sum(home_games) / len(home_games) if home_games else 0
        away_avg = sum(away_games) / len(away_games) if away_games else 0

        return jsonify({
            'points_per_game': points_per_game,
            'recent_performance': recent_performance,
            'matchup_history': matchup_points,
            'home_avg': home_avg,
            'away_avg': away_avg,
            'player_team_abbreviation': player_team_abbreviation,
            'opponent_team_abbreviation': opponent_team_abbreviation
        })

    except Exception as e:
        app.logger.error(f"Error in /points route: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
