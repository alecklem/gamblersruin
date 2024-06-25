# flask-server/app/etl.py
import sys
import os
import requests
import logging
from nba_api.stats.endpoints import (playerindex, leaguegamelog, playergamelog, playerdashboardbygeneralsplits, 
                                     commonteamyears, boxscoretraditionalv2, leaguegamefinder, playerestimatedmetrics, teamestimatedmetrics)

# Add the flask-server directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'flask-server')))

from app import db, create_app
from app.models import Player, Team, Game, PlayerGameLog, PlayerEstimatedMetrics, TeamEstimatedMetrics
from sqlalchemy.exc import IntegrityError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = create_app()

def load_players():
    logger.info("Starting to load players...")
    player_index = playerindex.PlayerIndex().get_normalized_dict()
    players = player_index['PlayerIndex']

    for player in players:
        try:
            existing_player = Player.query.filter_by(person_id=player['PERSON_ID']).first()
            if existing_player:
                logger.info(f"Player already exists: {player['PLAYER_FIRST_NAME']} {player['PLAYER_LAST_NAME']}")
                continue
            
            player_dashboard = playerdashboardbygeneralsplits.PlayerDashboardByGeneralSplits(player_id=player['PERSON_ID'], season="2023-24").get_normalized_dict()
            season_avg = player_dashboard['OverallPlayerDashboard'][0] if player_dashboard['OverallPlayerDashboard'] else {}

            db_player = Player(
                person_id=player['PERSON_ID'],
                last_name=player['PLAYER_LAST_NAME'],
                first_name=player['PLAYER_FIRST_NAME'],
                team_id=player['TEAM_ID'],
                team_abbreviation=player['TEAM_ABBREVIATION'],
                position=player['POSITION'],
                height=player['HEIGHT'],
                weight=player['WEIGHT'],
                college=player['COLLEGE'],
                country=player['COUNTRY'],
                draft_year=player['DRAFT_YEAR'],
                draft_round=player['DRAFT_ROUND'],
                draft_number=player['DRAFT_NUMBER'],
                pts=player['PTS'],
                reb=player['REB'],
                ast=player['AST'],
                season_avg_pts=season_avg.get('PTS', 0),
                season_avg_reb=season_avg.get('REB', 0),
                season_avg_ast=season_avg.get('AST', 0)
            )
            db.session.merge(db_player)
            db.session.commit()
            logger.info(f"Loaded player: {player['PLAYER_FIRST_NAME']} {player['PLAYER_LAST_NAME']}")
        except IntegrityError:
            db.session.rollback()
            logger.error(f"Error loading player: {player['PLAYER_FIRST_NAME']} {player['PLAYER_LAST_NAME']}")

def load_teams():
    logger.info("Starting to load teams...")
    team_years = commonteamyears.CommonTeamYears().get_normalized_dict()
    teams = team_years['TeamYears']
    
    for team in teams:
        try:
            existing_team = Team.query.filter_by(team_id=team['TEAM_ID']).first()
            if existing_team:
                logger.info(f"Team already exists: {team['ABBREVIATION']}")
                continue

            db_team = Team(
                team_id=team['TEAM_ID'],
                team_city=team['TEAM_CITY'],
                team_name=team['TEAM_NAME'],
                team_abbreviation=team['ABBREVIATION']
            )
            db.session.merge(db_team)
            db.session.commit()
            logger.info(f"Loaded team: {team['TEAM_NAME']}")
        except IntegrityError:
            db.session.rollback()
            logger.error(f"Error loading team: {team['TEAM_NAME']}")

def load_games():
    logger.info("Starting to load games...")
    game_log = leaguegamelog.LeagueGameLog(season="2023-24").get_normalized_dict()
    games = game_log['LeagueGameLog']

    for game in games:
        try:
            # Fetch the box score for the game to get the team stats
            box_score = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game['GAME_ID']).get_normalized_dict()

            if 'TeamStats' not in box_score:
                logger.error(f"KeyError: 'TeamStats' in game log for game: {game['GAME_ID']}")
                continue

            team_stats = box_score['TeamStats']

            for team_stat in team_stats:
                db_game = Game.query.filter_by(game_id=team_stat['GAME_ID'], team_id=str(team_stat['TEAM_ID'])).first()
                
                # Transform the min field to fit the length and format to two decimal places
                formatted_min = team_stat['MIN'][:6]

                transformed_team_name = team_stat['TEAM_NAME'][:100] if len(team_stat['TEAM_NAME']) > 100 else team_stat['TEAM_NAME']
                transformed_team_city = team_stat['TEAM_CITY'][:100] if len(team_stat['TEAM_CITY']) > 100 else team_stat['TEAM_CITY']

                if db_game:
                    db_game.team_name = transformed_team_name
                    db_game.team_abbreviation = team_stat['TEAM_ABBREVIATION']
                    db_game.team_city = transformed_team_city
                    db_game.min = formatted_min
                    db_game.fgm = team_stat['FGM']
                    db_game.fga = team_stat['FGA']
                    db_game.fg_pct = team_stat['FG_PCT']
                    db_game.fg3m = team_stat['FG3M']
                    db_game.fg3a = team_stat['FG3A']
                    db_game.fg3_pct = team_stat['FG3_PCT']
                    db_game.ftm = team_stat['FTM']
                    db_game.fta = team_stat['FTA']
                    db_game.ft_pct = team_stat['FT_PCT']
                    db_game.oreb = team_stat['OREB']
                    db_game.dreb = team_stat['DREB']
                    db_game.reb = team_stat['REB']
                    db_game.ast = team_stat['AST']
                    db_game.stl = team_stat['STL']
                    db_game.blk = team_stat['BLK']
                    db_game.to = team_stat['TO']
                    db_game.pf = team_stat['PF']
                    db_game.pts = team_stat['PTS']
                    db_game.plus_minus = team_stat['PLUS_MINUS']
                else:
                    db_game = Game(
                        game_id=team_stat['GAME_ID'],
                        team_id=str(team_stat['TEAM_ID']),
                        team_name=transformed_team_name,
                        team_abbreviation=team_stat['TEAM_ABBREVIATION'],
                        team_city=transformed_team_city,
                        min=formatted_min,
                        fgm=team_stat['FGM'],
                        fga=team_stat['FGA'],
                        fg_pct=team_stat['FG_PCT'],
                        fg3m=team_stat['FG3M'],
                        fg3a=team_stat['FG3A'],
                        fg3_pct=team_stat['FG3_PCT'],
                        ftm=team_stat['FTM'],
                        fta=team_stat['FTA'],
                        ft_pct=team_stat['FT_PCT'],
                        oreb=team_stat['OREB'],
                        dreb=team_stat['DREB'],
                        reb=team_stat['REB'],
                        ast=team_stat['AST'],
                        stl=team_stat['STL'],
                        blk=team_stat['BLK'],
                        to=team_stat['TO'],
                        pf=team_stat['PF'],
                        pts=team_stat['PTS'],
                        plus_minus=team_stat['PLUS_MINUS']
                    )

                db.session.merge(db_game)
                db.session.commit()
                logger.info(f"Loaded game stats for game: {team_stat['GAME_ID']} and team: {team_stat['TEAM_ABBREVIATION']}")
        except IntegrityError:
            db.session.rollback()
            logger.error(f"Error loading game stats for game: {game['GAME_ID']}")
        except KeyError as e:
            logger.error(f"KeyError: {e} in game log for game: {game['GAME_ID']}")
        except ValueError as e:
            logger.error(f"ValueError: {e} in game log for game: {game['GAME_ID']}")

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10), retry=retry_if_exception_type(requests.exceptions.RequestException))
def fetch_player_game_log(player_id):
    return playergamelog.PlayerGameLog(player_id=player_id, season="2023-24").get_normalized_dict()

def load_player_game_logs():
    logger.info("Starting to load player game logs...")
    players = Player.query.all()
    
    for player in players:
        try:
            game_logs = fetch_player_game_log(player.person_id)
            player_games = game_logs['PlayerGameLog']
            
            for game in player_games:
                existing_log = PlayerGameLog.query.filter_by(game_id=game['Game_ID'], player_id=str(player.person_id)).first()

                is_home_game = not game['MATCHUP'].startswith('@')
                game_date = datetime.strptime(game['GAME_DATE'], '%b %d, %Y').date()
                if existing_log:
                    # Update the existing log with additional information
                    existing_log.season_id = game['SEASON_ID']
                    existing_log.game_date = game_date
                    existing_log.matchup = game['MATCHUP']
                    existing_log.wl = game['WL']
                    existing_log.minutes = game['MIN']
                    existing_log.fgm = game['FGM']
                    existing_log.fga = game['FGA']
                    existing_log.fg_pct = game['FG_PCT']
                    existing_log.fg3m = game['FG3M']
                    existing_log.fg3a = game['FG3A']
                    existing_log.fg3_pct = game['FG3_PCT']
                    existing_log.ftm = game['FTM']
                    existing_log.fta = game['FTA']
                    existing_log.ft_pct = game['FT_PCT']
                    existing_log.oreb = game['OREB']
                    existing_log.dreb = game['DREB']
                    existing_log.rebounds = game['REB']
                    existing_log.assists = game['AST']
                    existing_log.stl = game['STL']
                    existing_log.blk = game['BLK']
                    existing_log.tov = game['TOV']
                    existing_log.pf = game['PF']
                    existing_log.points = game['PTS']
                    existing_log.plus_minus = game['PLUS_MINUS']
                    existing_log.video_available = game['VIDEO_AVAILABLE'] == 1
                    existing_log.is_home_game = is_home_game
                else:
                    db_player_game_log = PlayerGameLog(
                        game_id=game['Game_ID'],
                        player_id=str(player.person_id),
                        season_id=game['SEASON_ID'],
                        game_date=game_date,
                        matchup=game['MATCHUP'],
                        wl=game['WL'],
                        minutes=game['MIN'],
                        fgm=game['FGM'],
                        fga=game['FGA'],
                        fg_pct=game['FG_PCT'],
                        fg3m=game['FG3M'],
                        fg3a=game['FG3A'],
                        fg3_pct=game['FG3_PCT'],
                        ftm=game['FTM'],
                        fta=game['FTA'],
                        ft_pct=game['FT_PCT'],
                        oreb=game['OREB'],
                        dreb=game['DREB'],
                        rebounds=game['REB'],
                        assists=game['AST'],
                        stl=game['STL'],
                        blk=game['BLK'],
                        tov=game['TOV'],
                        pf=game['PF'],
                        points=game['PTS'],
                        plus_minus=game['PLUS_MINUS'],
                        video_available=game['VIDEO_AVAILABLE'] == 1,
                        is_home_game=is_home_game
                    )
                    db.session.add(db_player_game_log)
            db.session.commit()
            logger.info(f"Loaded game logs for player: {player.first_name} {player.last_name}")
        except IntegrityError:
            db.session.rollback()
            logger.error(f"Error loading game logs for player: {player.first_name} {player.last_name}")
        except KeyError as e:
            logger.error(f"KeyError: {e} in game log for player: {player.first_name} {player.last_name}")
        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException: {e} when fetching game logs for player: {player.first_name} {player.last_name}")

def update_game_dates():
    gamefinder = leaguegamefinder.LeagueGameFinder()
    games_dict = gamefinder.get_dict()

    with app.app_context():
        for game in games_dict['resultSets'][0]['rowSet']:
            game_id = game[4]  # Adjusted index for GAME_ID
            game_date_str = game[5]  # Adjusted index for GAME_DATE
            print(f"Game ID: {game_id}, Game Date String: {game_date_str}, Full Game Data: {game}")  # Print the full game data for inspection

            try:
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
        game_logs = PlayerGameLog.query.all()

        for log in game_logs:
            if ' vs. ' in log.matchup:
                log.is_home_game = True
            elif ' @ ' in log.matchup:
                log.is_home_game = False
            else:
                print(f"Unexpected matchup format: {log.matchup}")

            db.session.add(log)
        
        db.session.commit()

def fetch_and_store_player_estimated_metrics():
    player_metrics_response = playerestimatedmetrics.PlayerEstimatedMetrics()
    player_metrics = player_metrics_response.get_dict()

    for player in player_metrics['resultSet']['rowSet']:
        player_id = player[0]  # Adjust the index based on the actual data structure
        metrics = {key: value for key, value in zip(player_metrics['resultSet']['headers'], player)}

        existing_record = PlayerEstimatedMetrics.query.filter_by(player_id=player_id).first()
        if existing_record:
            existing_record.metrics = metrics
        else:
            new_record = PlayerEstimatedMetrics(player_id=player_id, metrics=metrics)
            db.session.add(new_record)

    db.session.commit()

def fetch_and_store_team_estimated_metrics():
    team_metrics_response = teamestimatedmetrics.TeamEstimatedMetrics()
    team_metrics = team_metrics_response.get_dict()

    for team in team_metrics['resultSet']['rowSet']:
        team_id = team[1]  # Adjust the index based on the actual data structure
        metrics = {key: value for key, value in zip(team_metrics['resultSet']['headers'], team)}

        existing_record = TeamEstimatedMetrics.query.filter_by(team_id=team_id).first()
        if existing_record:
            existing_record.metrics = metrics
        else:
            new_record = TeamEstimatedMetrics(team_id=team_id, metrics=metrics)
            db.session.add(new_record)

    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        # load_players()
        # load_teams()
        # load_games()
        # load_player_game_logs()
        # update_game_dates()
        # update_is_home_game()
        fetch_and_store_team_estimated_metrics()
        fetch_and_store_player_estimated_metrics()
