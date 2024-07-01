import sys
import os
import requests
import logging
from nba_api.stats.endpoints import (
    playerindex, leaguegamelog, playergamelog, playerdashboardbygeneralsplits, 
    commonteamyears, boxscoretraditionalv2, leaguegamefinder, playerestimatedmetrics, 
    teamestimatedmetrics, cumestatsplayer, playerdashptpass, playerdashptreb, playerdashptshotdefend,
    playerdashptshots, shotchartdetail, synergyplaytypes
)
# Add the flask-server directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'flask-server')))

from app import db, create_app
from app.models import (
    Player, Team, Game, PlayerGameLog, PlayerEstimatedMetrics, 
    TeamEstimatedMetrics, Cumestats, Playerdshptpass, Playerdshptreb, 
    Playerdshptdefend, Playerdshptshots, Shotchartdetail, Synergyplaytypes
)
from sqlalchemy.exc import IntegrityError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = create_app()

@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=4, max=10), retry=retry_if_exception_type(requests.exceptions.RequestException))
def fetch_and_insert_data(endpoint, model, column_mapping, params=None, additional_params=None):
    if params is None:
        params = {}
    if additional_params is None:
        additional_params = {}
    
    data = endpoint(**params, **additional_params).get_data_frames()[0]

    with app.app_context():
        for row in data.to_dict('records'):
            mapped_row = {model_column: row[api_column] for model_column, api_column in column_mapping.items()}
            db_entry = model(**mapped_row)
            db.session.merge(db_entry)
            db.session.commit()
            logger.info(f"Inserted row for {model.__name__}: {mapped_row}")

@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=4, max=10), retry=retry_if_exception_type(requests.exceptions.RequestException))
def load_cumestats():
    logger.info("Starting to load cumulative stats...")
    
    players = Player.query.all()
    
    for player in players:
        try:
            # Fetch all game IDs for the player from PlayerGameLog
            game_logs = PlayerGameLog.query.filter_by(player_id=str(player.person_id)).all()
            game_ids = [log.game_id for log in game_logs]

            if not game_ids:
                logger.warning(f"No game IDs found for player {player.person_id}")
                continue
            
            # Fetch cumulative stats for each player
            response = cumestatsplayer.CumeStatsPlayer(player_id=player.person_id, game_ids=game_ids).get_data_frames()[1]  # Use index 1 for total_player_stats
            
            # Debug: print the keys of the first row in the response
            if not response.empty:
                logger.debug(f"Response keys for player {player.person_id}: {response.columns.tolist()}")
            else:
                logger.warning(f"Empty response for player {player.person_id}")
                continue

            for row in response.to_dict('records'):
                db_entry = Cumestats(
                    player_id=row.get('PERSON_ID', player.person_id),
                    season_id=row.get('SEASON_ID', ''),
                    games_played=row.get('GP', None),
                    games_started=row.get('GS', None),
                    actual_minutes=row.get('ACTUAL_MINUTES', None),
                    actual_seconds=row.get('ACTUAL_SECONDS', None),
                    fg=row.get('FG', None),
                    fga=row.get('FGA', None),
                    fg_pct=row.get('FG_PCT', None),
                    fg3=row.get('FG3', None),
                    fg3a=row.get('FG3A', None),
                    fg3_pct=row.get('FG3_PCT', None),
                    ft=row.get('FT', None),
                    fta=row.get('FTA', None),
                    ft_pct=row.get('FT_PCT', None),
                    off_reb=row.get('OFF_REB', None),
                    def_reb=row.get('DEF_REB', None),
                    tot_reb=row.get('TOT_REB', None),
                    ast=row.get('AST', None),
                    pf=row.get('PF', None),
                    dq=row.get('DQ', None),
                    stl=row.get('STL', None),
                    turnovers=row.get('TURNOVERS', None),
                    blk=row.get('BLK', None),
                    pts=row.get('PTS', None),
                    max_actual_minutes=row.get('MAX_ACTUAL_MINUTES', None),
                    max_actual_seconds=row.get('MAX_ACTUAL_SECONDS', None),
                    max_reb=row.get('MAX_REB', None),
                    max_ast=row.get('MAX_AST', None),
                    max_stl=row.get('MAX_STL', None),
                    max_turnovers=row.get('MAX_TURNOVERS', None),
                    max_blk=row.get('MAX_BLK', None),
                    max_pts=row.get('MAX_PTS', None),
                    avg_actual_minutes=row.get('AVG_ACTUAL_MINUTES', None),
                    avg_actual_seconds=row.get('AVG_ACTUAL_SECONDS', None),
                    avg_tot_reb=row.get('AVG_TOT_REB', None),
                    avg_ast=row.get('AVG_AST', None),
                    avg_stl=row.get('AVG_STL', None),
                    avg_turnovers=row.get('AVG_TURNOVERS', None),
                    avg_blk=row.get('AVG_BLK', None),
                    avg_pts=row.get('AVG_PTS', None),
                    per_min_tot_reb=row.get('PER_MIN_TOT_REB', None),
                    per_min_ast=row.get('PER_MIN_AST', None),
                    per_min_stl=row.get('PER_MIN_STL', None),
                    per_min_turnovers=row.get('PER_MIN_TURNOVERS', None),
                    per_min_blk=row.get('PER_MIN_BLK', None),
                    per_min_pts=row.get('PER_MIN_PTS', None)
                )
                db.session.merge(db_entry)
                db.session.commit()
                logger.info(f"Inserted row for Cumestats: {db_entry}")
        except IntegrityError:
            db.session.rollback()
            logger.error(f"Integrity error for player {player.person_id}")
        except Exception as e:
            logger.error(f"Error loading cumulative stats for player {player.person_id}: {e}")



def load_playerdshptpass():
    logger.info("Starting to load player dashboard pass stats...")
    column_mapping = {
        'player_id': 'PLAYER_ID',
        'season_id': 'SEASON_ID',
        'passes_made': 'PASSES_MADE',
        'passes_received': 'PASSES_RECEIVED',
        'assists': 'ASSISTS',
        'secondary_assists': 'SECONDARY_ASSISTS',
        'potential_assists': 'POTENTIAL_ASSISTS'
    }

    players = Player.query.all()
    for player in players:
        try:
            params = {'team_id': player.team_id, 'player_id': player.person_id}
            fetch_and_insert_data(playerdashptpass.PlayerDashPtPass, Playerdshptpass, column_mapping, params)
        except Exception as e:
            logger.error(f"Error loading player dashboard pass stats for player {player.person_id}: {e}")

def load_playerdshptreb():
    logger.info("Starting to load player dashboard rebound stats...")
    column_mapping = {
        'player_id': 'PLAYER_ID',
        'season_id': 'SEASON_ID',
        'offensive_rebounds': 'OREB',
        'defensive_rebounds': 'DREB',
        'total_rebounds': 'REB'
    }

    players = Player.query.all()
    for player in players:
        try:
            params = {'team_id': player.team_id, 'player_id': player.person_id}
            fetch_and_insert_data(playerdashptreb.PlayerDashPtReb, Playerdshptreb, column_mapping, params)
        except Exception as e:
            logger.error(f"Error loading player dashboard rebound stats for player {player.person_id}: {e}")


@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=4, max=10), retry=retry_if_exception_type(requests.exceptions.RequestException))
def fetch_data_with_retry(params):
    try:
        return playerdashptshotdefend.PlayerDashPtShotDefend(**params, timeout=60).get_data_frames()[0]
    except Exception as e:
        logger.error(f"Error fetching data for params {params}: {e}")
        raise


@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=4, max=10), retry=retry_if_exception_type(requests.exceptions.RequestException))
def load_playerdshptdefend():
    logger.info("Starting to load player dashboard defend stats...")

    column_mapping = {
        'player_id': 'PLAYER_ID',
        'season_id': 'SEASON_ID',
        'close_def_person_id': 'CLOSE_DEF_PLAYER_ID',
        'gp': 'GP',
        'g': 'G',
        'defense_category': 'DEFENSE_CATEGORY',
        'freq': 'FREQ',
        'd_fgm': 'D_FGM',
        'd_fga': 'D_FGA',
        'd_fg_pct': 'D_FG_PCT',
        'normal_fg_pct': 'NORMAL_FG_PCT',
        'pct_plusminus': 'PCT_PLUSMINUS'
    }
    current_season_id = "2023-24"

    players = Player.query.all()
    for player in players:
        try:
            params = {
                'player_id': player.person_id,
                'team_id': player.team_id,
                'season': current_season_id,
                'per_mode_simple': 'Totals',
                'season_type_all_star': 'Regular Season'
            }
            data = fetch_data_with_retry(params)
            
            # Ensure the PLAYER_ID and CLOSE_DEF_PLAYER_ID columns are present
            if 'PLAYER_ID' not in data.columns:
                data['PLAYER_ID'] = player.person_id
            if 'CLOSE_DEF_PLAYER_ID' not in data.columns:
                data['CLOSE_DEF_PLAYER_ID'] = data['PLAYER_ID']

            # Add SEASON_ID column
            data['SEASON_ID'] = current_season_id

            # Debug: log the data received
            logger.debug(f"Data for player {player.person_id}: {data.head()}")

            with app.app_context():
                for row in data.to_dict('records'):
                    row['SEASON_ID'] = current_season_id
                    row['PLAYER_ID'] = player.person_id  # Ensure player_id is set

                    # Debug: log each row before mapping
                    logger.debug(f"Row before mapping: {row}")
                    mapped_row = {model_column: row.get(api_column) for model_column, api_column in column_mapping.items()}
                    # Ensure mandatory fields are present
                    if not mapped_row['player_id'] or not mapped_row['season_id']:
                        logger.error(f"Missing player_id or season_id in row: {row}")
                        continue

                    # print(mapped_row['d_fgm'])

                    # if mapped_row['freq'] == 'nan':
                    #     mapped_row['freq'] = 0
                    # if mapped_row['d_fgm'] == 'nan':
                    #     mapped_row['d_fgm'] = 0
                    # if mapped_row['d_fga'] == 'nan':
                    #     mapped_row['d_fga'] = 0
                    # if mapped_row['d_fg_pct'] == 'nan':
                    #     mapped_row['d_fg_pct'] = 0
                    # if mapped_row['pct_plusminus'] == 'nan':
                    #     mapped_row['pct_plusminus'] = 0

                    # Debug: log each mapped row
                    logger.debug(f"Mapped row: {mapped_row}")
                    db_entry = Playerdshptdefend(**mapped_row)
                    db.session.merge(db_entry)
                    db.session.commit()
                    logger.info(f"Inserted row for Playerdshptdefend: {mapped_row}")
        except IntegrityError as e:
            db.session.rollback()
            logger.error(f"Integrity error for player {player.person_id}: {e}")
        except Exception as e:
            logger.error(f"Error loading player dashboard defend stats for player {player.person_id}: {e}")


def load_playerdshptshots():
    logger.info("Starting to load player dashboard shot stats...")
    column_mapping = {
        'player_id': 'PLAYER_ID',
        'season_id': 'SEASON_ID',
        'shot_type': 'SHOT_TYPE',
        'shot_zone': 'SHOT_ZONE',
        'fgm': 'FGM',
        'fga': 'FGA',
        'fg_pct': 'FG_PCT'
    }

    players = Player.query.all()
    for player in players:
        try:
            params = {'team_id': player.team_id, 'player_id': player.person_id}
            fetch_and_insert_data(playerdashptshots.PlayerDashPtShots, Playerdshptshots, column_mapping, params)
        except Exception as e:
            logger.error(f"Error loading player dashboard shot stats for player {player.person_id}: {e}")

def load_shotchartdetail():
    logger.info("Starting to load shot chart details...")
    column_mapping = {
        'player_id': 'PLAYER_ID',
        'game_id': 'GAME_ID',
        'team_id': 'TEAM_ID',
        'shot_attempted_flag': 'SHOT_ATTEMPTED_FLAG',
        'shot_made_flag': 'SHOT_MADE_FLAG',
        'shot_zone_basic': 'SHOT_ZONE_BASIC',
        'shot_zone_area': 'SHOT_ZONE_AREA',
        'shot_zone_range': 'SHOT_ZONE_RANGE',
        'shot_distance': 'SHOT_DISTANCE',
        'loc_x': 'LOC_X',
        'loc_y': 'LOC_Y',
        'shot_attempted_date': 'GAME_DATE'
    }

    players = Player.query.all()
    for player in players:
        try:
            params = {'player_id': player.person_id, 'game_id': '', 'team_id': player.team_id}  # Adjust game_id as needed
            fetch_and_insert_data(shotchartdetail.ShotChartDetail, Shotchartdetail, column_mapping, params)
        except Exception as e:
            logger.error(f"Error loading shot chart details for player {player.person_id}: {e}")

def load_synergyplaytypes():
    logger.info("Starting to load synergy play types...")
    column_mapping = {
        'player_id': 'PLAYER_ID',
        'play_type': 'PLAY_TYPE',
        'possession': 'POSS',
        'points': 'PTS',
        'field_goals_made': 'FGM',
        'field_goals_attempted': 'FGA',
        'points_per_possession': 'PPP'
    }

    players = Player.query.all()
    for player in players:
        try:
            params = {'player_id': player.person_id}
            fetch_and_insert_data(synergyplaytypes.SynergyPlayTypes, Synergyplaytypes, column_mapping, params)
        except Exception as e:
            logger.error(f"Error loading synergy play types for player {player.person_id}: {e}")

if __name__ == '__main__':
    with app.app_context():
        # load_players()
        # load_teams()
        # load_games()
        # load_player_game_logs()
        # update_game_dates()
        # update_is_home_game()
        # fetch_and_store_team_estimated_metrics()
        # fetch_and_store_player_estimated_metrics()
        # load_cumestats()
        # load_playerdshptpass()
        # load_playerdshptreb()
        load_playerdshptdefend()
        # load_playerdshptshots()
        # load_shotchartdetail()
        # load_synergyplaytypes()
