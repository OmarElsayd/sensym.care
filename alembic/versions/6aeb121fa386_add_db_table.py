"""add_db_table

Revision ID: 6aeb121fa386
Revises: 
Create Date: 2023-01-15 15:20:10.744689

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6aeb121fa386'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('password', sa.String(length=50), nullable=True),
    sa.Column('role', postgresql.ENUM('admin', 'doctor', 'client', name='role'), nullable=True),
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
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('session_id', sa.Integer(), nullable=False),
    sa.Column('recording_time', sa.String(length=50), nullable=False),
    sa.Column('recording_path', sa.String(length=100), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['session_id'], ['voice_analysis.sessions.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['voice_analysis.users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='voice_analysis'
    )
    op.create_table('annotations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('session_id', sa.Integer(), nullable=False),
    sa.Column('recording_id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.String(length=50), nullable=False),
    sa.Column('end_time', sa.String(length=50), nullable=False),
    sa.Column('label', sa.String(length=50), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['recording_id'], ['voice_analysis.recordings.id'], ),
    sa.ForeignKeyConstraint(['session_id'], ['voice_analysis.sessions.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='voice_analysis'
    )
    op.create_table('emotion_analysis',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('recording_id', sa.Integer(), nullable=False),
    sa.Column('session_id', sa.Integer(), nullable=False),
    sa.Column('emotion', postgresql.ENUM('Anger', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral', name='emotion'), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['recording_id'], ['voice_analysis.recordings.id'], ),
    sa.ForeignKeyConstraint(['session_id'], ['voice_analysis.sessions.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='voice_analysis'
    )
    op.create_table('transcriptions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('recording_id', sa.Integer(), nullable=False),
    sa.Column('session_id', sa.Integer(), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['recording_id'], ['voice_analysis.recordings.id'], ),
    sa.ForeignKeyConstraint(['session_id'], ['voice_analysis.sessions.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='voice_analysis'
    )
    op.create_table('voice_peaks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('recording_id', sa.Integer(), nullable=False),
    sa.Column('session_id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.String(length=50), nullable=False),
    sa.Column('end_time', sa.String(length=50), nullable=False),
    sa.Column('label', sa.String(length=50), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['recording_id'], ['voice_analysis.recordings.id'], ),
    sa.ForeignKeyConstraint(['session_id'], ['voice_analysis.sessions.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='voice_analysis'
    )
    op.create_table('word_associations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('recording_id', sa.Integer(), nullable=False),
    sa.Column('session_id', sa.Integer(), nullable=False),
    sa.Column('word', sa.String(length=50), nullable=False),
    sa.Column('association', sa.String(length=50), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['recording_id'], ['voice_analysis.recordings.id'], ),
    sa.ForeignKeyConstraint(['session_id'], ['voice_analysis.sessions.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='voice_analysis'
    )
    op.create_table('ml_models',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('model', postgresql.ENUM('NaiveBayesClassifiers', 'SupportVectorMachines', 'RecurrentNeuralNetworks', 'ConvolutionalNeuralNetworks', 'Transformer_models', name='machinelearningmodel'), nullable=False),
    sa.Column('word_associations_id', sa.Integer(), nullable=False),
    sa.Column('recording_id', sa.Integer(), nullable=False),
    sa.Column('peak_id', sa.Integer(), nullable=False),
    sa.Column('sentiment_id', sa.Integer(), nullable=False),
    sa.Column('transcription_id', sa.Integer(), nullable=False),
    sa.Column('annotation_id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['annotation_id'], ['voice_analysis.annotations.id'], ),
    sa.ForeignKeyConstraint(['peak_id'], ['voice_analysis.voice_peaks.id'], ),
    sa.ForeignKeyConstraint(['recording_id'], ['voice_analysis.recordings.id'], ),
    sa.ForeignKeyConstraint(['sentiment_id'], ['voice_analysis.emotion_analysis.id'], ),
    sa.ForeignKeyConstraint(['transcription_id'], ['voice_analysis.transcriptions.id'], ),
    sa.ForeignKeyConstraint(['word_associations_id'], ['voice_analysis.word_associations.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='voice_analysis'
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ml_models', schema='voice_analysis')
    op.drop_table('word_associations', schema='voice_analysis')
    op.drop_table('voice_peaks', schema='voice_analysis')
    op.drop_table('transcriptions', schema='voice_analysis')
    op.drop_table('emotion_analysis', schema='voice_analysis')
    op.drop_table('annotations', schema='voice_analysis')
    op.drop_table('recordings', schema='voice_analysis')
    op.drop_table('sessions', schema='voice_analysis')
    op.drop_table('users', schema='voice_analysis')
    # ### end Alembic commands ###
