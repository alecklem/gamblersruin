from flask import Flask, jsonify, request
import requests
from flask_cors import CORS
from flask_caching import Cache
from nba_api.stats.static import players
from nba_api.stats.endpoints import playerdashboardbygeneralsplits, leaguegamelog, boxscoretraditionalv2, playerprofilev2, playerindex
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

season = HARD_CODED_SEASON
current_date = HARD_CODED_DATE

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
        playerID = (player["id"])
        player_dashboard = playerdashboardbygeneralsplits.PlayerDashboardByGeneralSplits(player_id=playerID, season="2023-24")
        player_stats = player_dashboard.get_normalized_dict()["OverallPlayerDashboard"][0]
        #1
        # Player points per game for season
        total_points = player_stats["PTS"]
        games_played = player_stats["GP"]
        points_per_game = total_points / games_played if games_played > 0 else 0

        print(f"Player Points Per Game: {points_per_game}")

        league_log = leaguegamelog.LeagueGameLog(season=HARD_CODED_SEASON).get_normalized_dict()

        next_game = None
        for game in league_log['LeagueGameLog']:
            game_date = datetime.strptime(game['GAME_DATE'], "%Y-%m-%d")
            if game_date > current_date:
                next_game = game
                break

        opponent_team_abbreviation = next_game["MATCHUP"].split()[-1]

        # Fetch team abbreviation from playerindex
        player_index = playerindex.PlayerIndex().get_normalized_dict()
        player_team_abbreviation = next((player['TEAM_ABBREVIATION'] for player in player_index['PlayerIndex'] if player['PERSON_ID'] == playerID), None)

        # #2 
        # # Last 5 games performance
        # # Get home team ID and away team ID for future stats
        # player_profile = playerprofilev2.PlayerProfileV2(player_id=playerID)
        # next_game_info = player_profile.get_normalized_dict()["NextGame"][0]
        # # Extract player team abbreviation
        # player_team_abbreviation = next_game_info["PLAYER_TEAM_ABBREVIATION"]
        # print(f"Team Abbreviation: {player_team_abbreviation}")
        # # Extract opponent team abbreviation
        # opponent_team_abbreviation = next_game_info["VS_TEAM_ABBREVIATION"]
        # print(f"Opponent Team Abbreviation: {opponent_team_abbreviation}")
        # # Extract next game details
        # print(f"Next Game Info: {next_game_info}")

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

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
