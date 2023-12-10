from datetime import datetime
from enum import Enum

from sqlalchemy.dialects.postgresql.base import ENUM
from sqlalchemy.orm import relationship

from sensym_models.voice_analysis_db.base import Base
from sqlalchemy import JSON, Column, Integer, String, DateTime, ForeignKey, Float, CheckConstraint, Text


class Emotion(Enum):
    Anger = "Anger"
    Disgust = "Disgust"
    Fear = "Fear"
    Happy = "Happy"
    Sad = "Sad"
    Surprise = "Surprise"
    Neutral = "Neutral"


class Role(Enum):
    admin = "Admin"
    doctor = "Doctor"
    client = "Client"


class MachineLearningModel(Enum):
    NaiveBayesClassifiers = "NaiveBayesClassifiers"
    SupportVectorMachines = "SupportVectorMachines"
    RecurrentNeuralNetworks = "RecurrentNeuralNetworks"
    ConvolutionalNeuralNetworks = "ConvolutionalNeuralNetworks"
    Transformer_models = "Transformer_models"


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    created = Column(DateTime, default=datetime.utcnow)


class Sessions(Base):
    __tablename__ = 'sessions'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('users.id'), nullable=False)
    created = Column(DateTime, default=datetime.utcnow)

    users = relationship('Users')


class Recordings(Base):
    __tablename__ = 'recordings'

    id = Column(Integer, primary_key=True)
    session_id = Column(ForeignKey('sessions.id'), nullable=False)
    recording_time = Column(String(50), nullable=False)
    recording_path = Column(String(100), nullable=False)
    created = Column(DateTime, default=datetime.utcnow)

    sessions = relationship('Sessions')


class Annotations(Base):
    __tablename__ = 'annotations'

    id = Column(Integer, primary_key=True)
    recording_id = Column(ForeignKey('recordings.id'), nullable=False)
    start_time = Column(String(50), nullable=False)
    end_time = Column(String(50), nullable=False)
    label = Column(String(50), nullable=False)
    confidence = (Float, CheckConstraint('confidence >= 0 and confidence <= 1'))
    created = Column(DateTime, default=datetime.utcnow)

    recordings = relationship('Recordings')


class Transcriptions(Base):
    __tablename__ = 'transcriptions'

    id = Column(Integer, primary_key=True)
    recording_id = Column(ForeignKey('recordings.id'), nullable=False)
    text = Column(Text, nullable=False)
    created = Column(DateTime, default=datetime.utcnow)

    recordings = relationship('Recordings')


class EmotionAnalysis(Base):
    __tablename__ = 'emotion_analysis'

    id = Column(Integer, primary_key=True)
    recording_id = Column(ForeignKey('recordings.id'), nullable=False)
    emotion = Column(ENUM(Emotion, name="emotion"), nullable=False)
    confidence = (Float, CheckConstraint('confidence >= 0 and confidence <= 1'))
    created = Column(DateTime, default=datetime.utcnow)

    recordings = relationship('Recordings')


class VoicePeaks(Base):
    __tablename__ = 'voice_peaks'

    id = Column(Integer, primary_key=True)
    recording_id = Column(ForeignKey('recordings.id'), nullable=False)
    start_time = Column(String(50), nullable=False)
    end_time = Column(String(50), nullable=False)
    label = Column(String(50), nullable=False)
    confidence = (Float, CheckConstraint('confidence >= 0 and confidence <= 1'))
    created = Column(DateTime, default=datetime.utcnow)

    recordings = relationship('Recordings')



class EmotionConfig(Base):
    __tablename__ = 'emotion_config'
    
    id = Column(Integer, primary_key=True)
    emotion_json_config = Column(JSON, nullable=False)
    created = Column(DateTime, default=datetime.utcnow)





