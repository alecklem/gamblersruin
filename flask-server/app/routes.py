from flask import current_app as app, jsonify, request
from app import db
from app.models import Player, Game, PlayerGameLog, PlayerEstimatedMetrics, TeamEstimatedMetrics, Team
from datetime import datetime, timedelta
from nba_api.stats.endpoints import playerestimatedmetrics, teamestimatedmetrics

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

        player_id = data.get('player', {}).get('id')
        if not player_id:
            app.logger.error("Player ID not provided")
            return jsonify({'error': 'Player ID not provided'}), 400

        player_id = str(player_id)

        player = Player.query.filter_by(person_id=player_id).first()
        if not player:
            app.logger.error(f"Player with ID {player_id} not found")
            return jsonify({'error': 'Player not found'}), 404

        points_per_game = round(player.pts, 2)
        player_team_abbreviation = player.team_abbreviation
        player_team_id = str(player.team_id)

        last_5_games = PlayerGameLog.query.filter_by(player_id=player_id).order_by(PlayerGameLog.game_date.desc()).limit(5).all()
        player_points_in_last_5_games = [game.points for game in last_5_games]
        last_5_game_dates = [game.game_date.strftime('%m/%d') for game in last_5_games]

        rest_days = []
        for i in range(len(last_5_games) - 1):
            diff_days = (last_5_games[i].game_date - last_5_games[i + 1].game_date).days - 1
            if diff_days == 0:
                rest_days.append("B2B")
            elif diff_days == 1:
                rest_days.append(f"{diff_days} day")
            else:
                rest_days.append(f"{diff_days} days")

        home_games = PlayerGameLog.query.filter_by(player_id=player_id, is_home_game=True).all()
        away_games = PlayerGameLog.query.filter_by(player_id=player_id, is_home_game=False).all()

        home_points = [game.points for game in home_games]
        away_points = [game.points for game in away_games]

        home_points_per_game = round(sum(home_points) / len(home_points), 2) if home_points else 0
        away_points_per_game = round(sum(away_points) / len(away_points), 2) if away_points else 0

        hardcoded_date = datetime(2024, 3, 15)

        next_game_entry = Game.query.filter(Game.game_date > hardcoded_date, Game.team_id == player_team_id).order_by(Game.game_date.asc()).first()
        if next_game_entry:
            opponent_game_entry = Game.query.filter(Game.game_id == next_game_entry.game_id, Game.team_id != player_team_id).first()
            opponent_team_abbreviation = opponent_game_entry.team_abbreviation
            opponent_team_id = opponent_game_entry.team_id
            games_against_opponent = PlayerGameLog.query.filter_by(player_id=player_id).filter(PlayerGameLog.game_id.in_(
                db.session.query(Game.game_id).filter(Game.team_id == opponent_team_id)
            )).all()
            player_points_against_opponent = [game.points for game in games_against_opponent]
            opponent_game_dates = [game.game_date.strftime('%m/%d') for game in games_against_opponent]
        else:
            opponent_team_abbreviation = "N/A"
            player_points_against_opponent = []
            opponent_game_dates = []

        # Fetch Player Estimated Metrics 
        player_metrics = PlayerEstimatedMetrics.query.filter_by(player_id=player_id).first()
        player_metrics_filtered = player_metrics.metrics if player_metrics else {}

        # Fetch Opponent Defensive Rating
        team_metrics = TeamEstimatedMetrics.query.filter_by(team_id=opponent_team_id).first() if next_game_entry else None
        team_metrics_filtered = team_metrics.metrics if team_metrics else {}

        player_team_colors = Team.query.filter_by(team_id=player_team_id).first().colors
        opponent_team_colors = Team.query.filter_by(team_id=opponent_team_id).first().colors

        return jsonify({
            'team_abbreviation': player_team_abbreviation,
            'points_per_game': points_per_game,
            'player_points_in_last_5_games': player_points_in_last_5_games[::-1],
            'last_5_game_dates': last_5_game_dates[::-1],
            'home_points_per_game': home_points_per_game,
            'away_points_per_game': away_points_per_game,
            'rest_days': rest_days[::-1],
            'player_points_against_opponent': player_points_against_opponent[::-1],
            'opponent_game_dates': opponent_game_dates[::-1],
            'opponent_team_abbreviation': opponent_team_abbreviation,
            'matchup': f"{player_team_abbreviation} vs {opponent_team_abbreviation}" if opponent_team_abbreviation != "N/A" else "N/A",
            'player_metrics': player_metrics_filtered,
            'team_metrics': team_metrics_filtered,
            "player_team_colors": player_team_colors,
            "opponent_team_colors": opponent_team_colors
        })
    except Exception as e:
        app.logger.error(f"Error in /points route: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/assists', methods=['POST'])
def assists():
    try:
        data = request.get_json()

        player_id = data.get('player', {}).get('id')
        if not player_id:
            app.logger.error("Player ID not provided")
            return jsonify({'error': 'Player ID not provided'}), 400

        player_id = str(player_id)  # Ensure player_id is a string

        player = Player.query.filter_by(person_id=player_id).first()
        if not player:
            app.logger.error(f"Player with ID {player_id} not found")
            return jsonify({'error': 'Player not found'}), 404

        assists_per_game = round(player.ast, 2)
        player_team_abbreviation = player.team_abbreviation
        player_team_id = str(player.team_id)  # Ensure team_id is a string

        # Fetch last 5 games performance
        last_5_games = PlayerGameLog.query.filter_by(player_id=player_id).order_by(PlayerGameLog.game_date.desc()).limit(5).all()
        player_assists_in_last_5_games = [game.assists for game in last_5_games]
        last_5_game_dates = [game.game_date.strftime('%m/%d') for game in last_5_games]

        # Calculate rest days based on last 5 games
        rest_days = []
        for i in range(len(last_5_games) - 1):
            diff_days = (last_5_games[i].game_date - last_5_games[i + 1].game_date).days - 1
            if diff_days == 0:
                rest_days.append("B2B")
            elif diff_days == 1:
                rest_days.append(f"{diff_days} day")
            else:
                rest_days.append(f"{diff_days} days")

        # Calculate home and away assists per game
        home_games = PlayerGameLog.query.filter_by(player_id=player_id, is_home_game=True).all()
        away_games = PlayerGameLog.query.filter_by(player_id=player_id, is_home_game=False).all()

        home_assists = [game.assists for game in home_games]
        away_assists = [game.assists for game in away_games]

        home_assists_per_game = round(sum(home_assists) / len(home_assists), 2) if home_assists else 0
        away_assists_per_game = round(sum(away_assists) / len(away_assists), 2) if away_assists else 0

        # Temporarily hardcode a date (e.g., March 15, 2024)
        hardcoded_date = datetime(2024, 3, 15)

        # Fetch performance against next opponent
        next_game_entry = Game.query.filter(Game.game_date > hardcoded_date, Game.team_id == player_team_id).order_by(Game.game_date.asc()).first()
        if next_game_entry:
            opponent_game_entry = Game.query.filter(Game.game_id == next_game_entry.game_id, Game.team_id != player_team_id).first()
            opponent_team_abbreviation = opponent_game_entry.team_abbreviation
            opponent_team_id = opponent_game_entry.team_id
            games_against_opponent = PlayerGameLog.query.filter_by(player_id=player_id).filter(PlayerGameLog.game_id.in_(
                db.session.query(Game.game_id).filter(Game.team_id == opponent_team_id)
            )).all()
            player_assists_against_opponent = [game.assists for game in games_against_opponent]
            opponent_game_dates = [game.game_date.strftime('%m/%d') for game in games_against_opponent]
        else:
            opponent_team_abbreviation = "N/A"
            player_assists_against_opponent = []
            opponent_game_dates = []

        # Fetch Player Estimated Metrics
        player_metrics = PlayerEstimatedMetrics.query.filter_by(player_id=player_id).first()
        player_metrics_filtered = player_metrics.metrics if player_metrics else {}

        # Fetch Opponent Defensive Rating
        team_metrics = TeamEstimatedMetrics.query.filter_by(team_id=opponent_team_id).first() if next_game_entry else None
        team_metrics_filtered = team_metrics.metrics if team_metrics else {}

        player_team_colors = Team.query.filter_by(team_id=player_team_id).first().colors
        opponent_team_colors = Team.query.filter_by(team_id=opponent_team_id).first().colors

        return jsonify({
            'team_abbreviation': player_team_abbreviation,
            'assists_per_game': assists_per_game,
            'player_assists_in_last_5_games': player_assists_in_last_5_games[::-1],  # Reverse order for frontend
            'last_5_game_dates': last_5_game_dates[::-1],  # Reverse order for frontend
            'home_assists_per_game': home_assists_per_game,
            'away_assists_per_game': away_assists_per_game,
            'rest_days': rest_days[::-1],  # Reverse order for frontend
            'player_assists_against_opponent': player_assists_against_opponent[::-1],  # Reverse order for frontend
            'opponent_game_dates': opponent_game_dates[::-1],  # Reverse order for frontend
            'opponent_team_abbreviation': opponent_team_abbreviation,
            'matchup': f"{player_team_abbreviation} vs {opponent_team_abbreviation}" if opponent_team_abbreviation != "N/A" else "N/A",
            'player_metrics': player_metrics_filtered,
            'team_metrics': team_metrics_filtered,
            "player_team_colors": player_team_colors,
            "opponent_team_colors": opponent_team_colors
        })
    except Exception as e:
        app.logger.error(f"Error in /assists route: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/rebounds', methods=['POST'])
def rebounds():
    try:
        data = request.get_json()

        player_id = data.get('player', {}).get('id')
        if not player_id:
            app.logger.error("Player ID not provided")
            return jsonify({'error': 'Player ID not provided'}), 400

        player_id = str(player_id)  # Ensure player_id is a string

        player = Player.query.filter_by(person_id=player_id).first()
        if not player:
            app.logger.error(f"Player with ID {player_id} not found")
            return jsonify({'error': 'Player not found'}), 404

        rebounds_per_game = round(player.reb, 2)
        player_team_abbreviation = player.team_abbreviation
        player_team_id = str(player.team_id)  # Ensure team_id is a string

        # Fetch last 5 games performance
        last_5_games = PlayerGameLog.query.filter_by(player_id=player_id).order_by(PlayerGameLog.game_date.desc()).limit(5).all()
        player_rebounds_in_last_5_games = [game.rebounds for game in last_5_games]
        last_5_game_dates = [game.game_date.strftime('%m/%d') for game in last_5_games]

        # Calculate rest days based on last 5 games
        rest_days = []
        for i in range(len(last_5_games) - 1):
            diff_days = (last_5_games[i].game_date - last_5_games[i + 1].game_date).days - 1
            if diff_days == 0:
                rest_days.append("B2B")
            elif diff_days == 1:
                rest_days.append(f"{diff_days} day")
            else:
                rest_days.append(f"{diff_days} days")

        # Calculate home and away rebounds per game
        home_games = PlayerGameLog.query.filter_by(player_id=player_id, is_home_game=True).all()
        away_games = PlayerGameLog.query.filter_by(player_id=player_id, is_home_game=False).all()

        home_rebounds = [game.rebounds for game in home_games]
        away_rebounds = [game.rebounds for game in away_games]

        home_rebounds_per_game = round(sum(home_rebounds) / len(home_rebounds), 2) if home_rebounds else 0
        away_rebounds_per_game = round(sum(away_rebounds) / len(away_rebounds), 2) if away_rebounds else 0

        # Temporarily hardcode a date (e.g., March 15, 2024)
        hardcoded_date = datetime(2024, 3, 15)

        # Fetch performance against next opponent
        next_game_entry = Game.query.filter(Game.game_date > hardcoded_date, Game.team_id == player_team_id).order_by(Game.game_date.asc()).first()
        if next_game_entry:
            opponent_game_entry = Game.query.filter(Game.game_id == next_game_entry.game_id, Game.team_id != player_team_id).first()
            opponent_team_abbreviation = opponent_game_entry.team_abbreviation
            opponent_team_id = opponent_game_entry.team_id
            games_against_opponent = PlayerGameLog.query.filter_by(player_id=player_id).filter(PlayerGameLog.game_id.in_(
                db.session.query(Game.game_id).filter(Game.team_id == opponent_team_id)
            )).all()
            player_rebounds_against_opponent = [game.rebounds for game in games_against_opponent]
            opponent_game_dates = [game.game_date.strftime('%m/%d') for game in games_against_opponent]
        else:
            opponent_team_abbreviation = "N/A"
            player_rebounds_against_opponent = []
            opponent_game_dates = []

        # Fetch Player Estimated Metrics
        player_metrics = PlayerEstimatedMetrics.query.filter_by(player_id=player_id).first()
        player_metrics_filtered = player_metrics.metrics if player_metrics else {}

        # Fetch Opponent Defensive Rating
        team_metrics = TeamEstimatedMetrics.query.filter_by(team_id=opponent_team_id).first() if next_game_entry else None
        team_metrics_filtered = team_metrics.metrics if team_metrics else {}

        player_team_colors = Team.query.filter_by(team_id=player_team_id).first().colors
        opponent_team_colors = Team.query.filter_by(team_id=opponent_team_id).first().colors

        return jsonify({
            'team_abbreviation': player_team_abbreviation,
            'rebounds_per_game': rebounds_per_game,
            'player_rebounds_in_last_5_games': player_rebounds_in_last_5_games[::-1],  # Reverse order for frontend
            'last_5_game_dates': last_5_game_dates[::-1],  # Reverse order for frontend
            'home_rebounds_per_game': home_rebounds_per_game,
            'away_rebounds_per_game': away_rebounds_per_game,
            'rest_days': rest_days[::-1],  # Reverse order for frontend
            'player_rebounds_against_opponent': player_rebounds_against_opponent[::-1],  # Reverse order for frontend
            'opponent_game_dates': opponent_game_dates[::-1],  # Reverse order for frontend
            'opponent_team_abbreviation': opponent_team_abbreviation,
            'matchup': f"{player_team_abbreviation} vs {opponent_team_abbreviation}" if opponent_team_abbreviation != "N/A" else "N/A",
            'player_metrics': player_metrics_filtered,
            'team_metrics': team_metrics_filtered,
            "player_team_colors": player_team_colors,
            "opponent_team_colors": opponent_team_colors
        })
    except Exception as e:
        app.logger.error(f"Error in /rebounds route: {e}")
        return jsonify({'error': str(e)}), 500
