"""newdbe

Revision ID: 7428b9eaef1f
Revises: 
Create Date: 2023-03-05 00:53:44.683550

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '7428b9eaef1f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('emotion_config',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('emotion_json_config', sa.JSON(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='voice_analysis'
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='voice_analysis'
    )
    op.create_table('sessions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['voice_analysis.users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='voice_analysis'
    )
    op.create_table('recordings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('session_id', sa.Integer(), nullable=False),
    sa.Column('recording_time', sa.String(length=50), nullable=False),
    sa.Column('recording_path', sa.String(length=100), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['session_id'], ['voice_analysis.sessions.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='voice_analysis'
    )
    op.create_table('annotations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('recording_id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.String(length=50), nullable=False),
    sa.Column('end_time', sa.String(length=50), nullable=False),
    sa.Column('label', sa.String(length=50), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['recording_id'], ['voice_analysis.recordings.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='voice_analysis'
    )
    op.create_table('emotion_analysis',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('recording_id', sa.Integer(), nullable=False),
    sa.Column('emotion', postgresql.ENUM('Anger', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral', name='emotion'), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['recording_id'], ['voice_analysis.recordings.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='voice_analysis'
    )
    op.create_table('transcriptions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('recording_id', sa.Integer(), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['recording_id'], ['voice_analysis.recordings.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='voice_analysis'
    )
    op.create_table('voice_peaks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('recording_id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.String(length=50), nullable=False),
    sa.Column('end_time', sa.String(length=50), nullable=False),
    sa.Column('label', sa.String(length=50), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['recording_id'], ['voice_analysis.recordings.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='voice_analysis'
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('voice_peaks', schema='voice_analysis')
    op.drop_table('transcriptions', schema='voice_analysis')
    op.drop_table('emotion_analysis', schema='voice_analysis')
    op.drop_table('annotations', schema='voice_analysis')
    op.drop_table('recordings', schema='voice_analysis')
    op.drop_table('sessions', schema='voice_analysis')
    op.drop_table('users', schema='voice_analysis')
    op.drop_table('emotion_config', schema='voice_analysis')
    # ### end Alembic commands ###