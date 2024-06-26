"""Initial migration.

Revision ID: 2ae39a738ca7
Revises: 
Create Date: 2024-06-10 17:18:31.785229

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2ae39a738ca7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('game',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('game_id', sa.String(length=20), nullable=False),
    sa.Column('game_date', sa.Date(), nullable=True),
    sa.Column('home_team_id', sa.Integer(), nullable=True),
    sa.Column('away_team_id', sa.Integer(), nullable=True),
    sa.Column('home_team_score', sa.Integer(), nullable=True),
    sa.Column('away_team_score', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('game_id')
    )
    op.create_table('player',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('person_id', sa.Integer(), nullable=False),
    sa.Column('last_name', sa.String(length=255), nullable=True),
    sa.Column('first_name', sa.String(length=255), nullable=True),
    sa.Column('team_id', sa.Integer(), nullable=True),
    sa.Column('team_abbreviation', sa.String(length=10), nullable=True),
    sa.Column('position', sa.String(length=50), nullable=True),
    sa.Column('height', sa.String(length=10), nullable=True),
    sa.Column('weight', sa.String(length=10), nullable=True),
    sa.Column('college', sa.String(length=255), nullable=True),
    sa.Column('country', sa.String(length=255), nullable=True),
    sa.Column('draft_year', sa.Integer(), nullable=True),
    sa.Column('draft_round', sa.Integer(), nullable=True),
    sa.Column('draft_number', sa.Integer(), nullable=True),
    sa.Column('pts', sa.Float(), nullable=True),
    sa.Column('reb', sa.Float(), nullable=True),
    sa.Column('ast', sa.Float(), nullable=True),
    sa.Column('season_avg_pts', sa.Float(), nullable=True),
    sa.Column('season_avg_reb', sa.Float(), nullable=True),
    sa.Column('season_avg_ast', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('person_id')
    )
    op.create_table('team',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('team_id', sa.Integer(), nullable=False),
    sa.Column('team_city', sa.String(length=255), nullable=True),
    sa.Column('team_name', sa.String(length=255), nullable=True),
    sa.Column('team_abbreviation', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('team_id')
    )
    op.create_table('player_game_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('game_id', sa.String(length=20), nullable=True),
    sa.Column('player_id', sa.Integer(), nullable=True),
    sa.Column('team_id', sa.Integer(), nullable=True),
    sa.Column('points', sa.Integer(), nullable=True),
    sa.Column('assists', sa.Integer(), nullable=True),
    sa.Column('rebounds', sa.Integer(), nullable=True),
    sa.Column('minutes', sa.String(length=10), nullable=True),
    sa.Column('is_home_game', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['game_id'], ['game.game_id'], ),
    sa.ForeignKeyConstraint(['player_id'], ['player.person_id'], ),
    sa.ForeignKeyConstraint(['team_id'], ['team.team_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('player_game_log')
    op.drop_table('team')
    op.drop_table('player')
    op.drop_table('game')
    # ### end Alembic commands ###
