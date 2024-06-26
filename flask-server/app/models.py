# flask-server/app/models.py
from app import db

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, unique=True, nullable=False)
    last_name = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    team_id = db.Column(db.Integer)
    team_abbreviation = db.Column(db.String(10))
    position = db.Column(db.String(50))
    height = db.Column(db.String(10))
    weight = db.Column(db.String(10))
    college = db.Column(db.String(255))
    country = db.Column(db.String(255))
    draft_year = db.Column(db.Integer)
    draft_round = db.Column(db.Integer)
    draft_number = db.Column(db.Integer)
    pts = db.Column(db.Float)
    reb = db.Column(db.Float)
    ast = db.Column(db.Float)
    season_avg_pts = db.Column(db.Float)
    season_avg_reb = db.Column(db.Float)
    season_avg_ast = db.Column(db.Float)

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, unique=True, nullable=False)
    team_city = db.Column(db.String(255))
    team_name = db.Column(db.String(255))
    team_abbreviation = db.Column(db.String(10))
    colors = db.Column(db.JSON)

class Game(db.Model):
    __tablename__ = 'game'
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.String(50), nullable=False)
    team_id = db.Column(db.String(50), nullable=False)
    team_name = db.Column(db.String(100), nullable=False)
    team_abbreviation = db.Column(db.String(10), nullable=False)
    team_city = db.Column(db.String(100), nullable=False)
    min = db.Column(db.String(10), nullable=True)
    fgm = db.Column(db.Integer, nullable=True)
    fga = db.Column(db.Integer, nullable=True)
    fg_pct = db.Column(db.Float, nullable=True)
    fg3m = db.Column(db.Integer, nullable=True)
    fg3a = db.Column(db.Integer, nullable=True)
    fg3_pct = db.Column(db.Float, nullable=True)
    ftm = db.Column(db.Integer, nullable=True)
    fta = db.Column(db.Integer, nullable=True)
    ft_pct = db.Column(db.Float, nullable=True)
    oreb = db.Column(db.Integer, nullable=True)
    dreb = db.Column(db.Integer, nullable=True)
    reb = db.Column(db.Integer, nullable=True)
    ast = db.Column(db.Integer, nullable=True)
    stl = db.Column(db.Integer, nullable=True)
    blk = db.Column(db.Integer, nullable=True)
    to = db.Column(db.Integer, nullable=True)
    pf = db.Column(db.Integer, nullable=True)
    pts = db.Column(db.Integer, nullable=True)
    plus_minus = db.Column(db.Float, nullable=True)
    game_date = db.Column(db.Date, nullable=True)

    __table_args__ = (db.UniqueConstraint('game_id', 'team_id', name='unique_game_team'),)

class PlayerGameLog(db.Model):
    __tablename__ = 'player_game_log'
    
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.String(50), nullable=False)
    player_id = db.Column(db.String(50), nullable=False)
    season_id = db.Column(db.String(10))
    game_date = db.Column(db.Date)
    matchup = db.Column(db.String(20))
    wl = db.Column(db.String(2))
    minutes = db.Column(db.String(10))
    fgm = db.Column(db.Integer)
    fga = db.Column(db.Integer)
    fg_pct = db.Column(db.Float)
    fg3m = db.Column(db.Integer)
    fg3a = db.Column(db.Integer)
    fg3_pct = db.Column(db.Float)
    ftm = db.Column(db.Integer)
    fta = db.Column(db.Integer)
    ft_pct = db.Column(db.Float)
    oreb = db.Column(db.Integer)
    dreb = db.Column(db.Integer)
    rebounds = db.Column(db.Integer)
    assists = db.Column(db.Integer)
    stl = db.Column(db.Integer)
    blk = db.Column(db.Integer)
    tov = db.Column(db.Integer)
    pf = db.Column(db.Integer)
    points = db.Column(db.Integer)
    plus_minus = db.Column(db.Float)
    video_available = db.Column(db.Boolean)
    is_home_game = db.Column(db.Boolean, nullable=False)


class PlayerEstimatedMetrics(db.Model):
    __tablename__ = 'player_estimated_metrics'
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    metrics = db.Column(db.JSON, nullable=False)  # Assuming metrics are stored in JSON format

class TeamEstimatedMetrics(db.Model):
    __tablename__ = 'team_estimated_metrics'
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    metrics = db.Column(db.JSON, nullable=False)  # Assuming metrics are stored in JSON format
