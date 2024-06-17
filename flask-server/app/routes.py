from flask import current_app as app, jsonify, request
from app import db
from app.models import Player, Game, PlayerGameLog
from datetime import datetime

@app.route('/loadplayers', methods=['GET'])
def load_players():
    try:
        players = Player.query.all()
        app.logger.info(f"Fetched players: {players}")
        player_list = [{
            'id': player.id,
            'person_id': player.person_id,
            'full_name': f"{player.first_name} {player.last_name}",
            'team_abbreviation': player.team_abbreviation,
        } for player in players]
        return jsonify(player_list)
    except Exception as e:
        app.logger.error(f"Error loading players: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/points', methods=['POST'])
def points():
    try:
        data = request.get_json()
        app.logger.info(f"Received data: {data}")
        
        player_id = data.get('player', {}).get('id')
        if not player_id:
            app.logger.error("Player ID not provided")
            return jsonify({'error': 'Player ID not provided'}), 400

        player_id = str(player_id)  # Ensure player_id is a string

        player = Player.query.filter_by(person_id=player_id).first()
        if not player:
            app.logger.error(f"Player with ID {player_id} not found")
            return jsonify({'error': 'Player not found'}), 404

        points_per_game = player.pts
        player_team_abbreviation = player.team_abbreviation

        # Fetch last 5 games performance
        last_5_games = PlayerGameLog.query.filter_by(player_id=player_id).order_by(PlayerGameLog.game_date.desc()).limit(5).all()
        player_points_in_last_5_games = [game.points for game in last_5_games]
        last_5_game_dates = [game.game_date.strftime('%Y-%m-%d') for game in last_5_games]
        app.logger.info(f"Last 5 games points: {player_points_in_last_5_games}")

        # Temporarily hardcode a date (e.g., March 1, 2024)
        hardcoded_date = datetime(2024, 3, 1)

        # Fetch performance against next opponent
        next_game_entry = Game.query.filter(Game.game_date > hardcoded_date).order_by(Game.game_date.asc()).first()
        
        if next_game_entry:
            opponent_team_abbreviation = next_game_entry.team_abbreviation
            opponent_team_id = next_game_entry.team_id
            games_against_opponent = PlayerGameLog.query.filter_by(player_id=player_id).filter(PlayerGameLog.game_id.in_(
                db.session.query(Game.game_id).filter(Game.team_id == opponent_team_id)
            )).all()
            player_points_against_opponent = [game.points for game in games_against_opponent]
            opponent_game_dates = [game.game_date.strftime('%Y-%m-%d') for game in games_against_opponent]
        else:
            opponent_team_abbreviation = "N/A"
            player_points_against_opponent = []
            opponent_game_dates = []

        return jsonify({
            'team_abbreviation': player_team_abbreviation,
            'opponent_team_abbreviation': opponent_team_abbreviation,
            'points_per_game': points_per_game,
            'player_points_in_last_5_games': player_points_in_last_5_games,
            'last_5_game_dates': last_5_game_dates,
            'player_points_against_opponent': player_points_against_opponent,
            'opponent_game_dates': opponent_game_dates,
            'matchup': f"{player_team_abbreviation} vs {opponent_team_abbreviation}" if opponent_team_abbreviation != "N/A" else "N/A"
        })


    except Exception as e:
        app.logger.error(f"Error in /points route: {e}")
        return jsonify({'error': str(e)}), 500
