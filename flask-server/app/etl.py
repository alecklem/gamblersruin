import sys
import os
from nba_api.stats.endpoints import leaguegamefinder
from datetime import datetime

# Adjust the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import Game, PlayerGameLog

app = create_app()

def update_game_dates():
    gamefinder = leaguegamefinder.LeagueGameFinder()
    games_dict = gamefinder.get_dict()

    with app.app_context():
        for game in games_dict['resultSets'][0]['rowSet']:
            game_id = game[4]  # Adjusted index for GAME_ID
            game_date_str = game[5]  # Adjusted index for GAME_DATE
            print(f"Game ID: {game_id}, Game Date String: {game_date_str}, Full Game Data: {game}")  # Print the full game data for inspection

            try:
                # The correct format for '2019-10-08' is '%Y-%m-%d'
                game_date = datetime.strptime(game_date_str, '%Y-%m-%d').date()
            except ValueError as e:
                print(f"Error parsing date: {e}")
                continue  # Skip this record if the date is invalid

            home_team_id = game[1]  # Adjusted index for TEAM_ID
            away_team_id = None  # Assuming away team ID can be found or is not needed for this context

            # Update or insert game date for home team
            game_home = Game.query.filter_by(game_id=game_id, team_id=str(home_team_id)).first()
            if game_home:
                game_home.game_date = game_date
                db.session.add(game_home)

            # Update or insert game date for away team if needed
            if away_team_id:
                game_away = Game.query.filter_by(game_id=game_id, team_id=str(away_team_id)).first()
                if game_away:
                    game_away.game_date = game_date
                    db.session.add(game_away)

        db.session.commit()

def update_is_home_game():
    with app.app_context():
        # Query all player game logs
        game_logs = PlayerGameLog.query.all()

        for log in game_logs:
            # Determine if the game is home or away based on the matchup string
            if ' vs. ' in log.matchup:
                log.is_home_game = True
            elif ' @ ' in log.matchup:
                log.is_home_game = False
            else:
                print(f"Unexpected matchup format: {log.matchup}")

            db.session.add(log)
        
        db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        update_is_home_game()
