from datetime import datetime
from enum import Enum

from sqlalchemy.dialects.postgresql.base import ENUM
from sqlalchemy.orm import relationship

from sensym_models.voice_analysis_db.base import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, CheckConstraint, Text


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
    name = Column(String(50))
    email = Column(String(50))
    password = Column(String(50))
    role = Column(ENUM(Role))
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
    user_id = Column(ForeignKey('users.id'), nullable=False)
    session_id = Column(ForeignKey('sessions.id'), nullable=False)
    recording_time = Column(String(50), nullable=False)
    recording_path = Column(String(100), nullable=False)
    created = Column(DateTime, default=datetime.utcnow)

    users = relationship('Users')
    sessions = relationship('Sessions')


class Annotations(Base):
    __tablename__ = 'annotations'

    id = Column(Integer, primary_key=True)
    session_id = Column(ForeignKey('sessions.id'), nullable=False)
    recording_id = Column(ForeignKey('recordings.id'), nullable=False)
    start_time = Column(String(50), nullable=False)
    end_time = Column(String(50), nullable=False)
    label = Column(String(50), nullable=False)
    confidence = (Float, CheckConstraint('confidence >= 0 and confidence <= 1'))
    created = Column(DateTime, default=datetime.utcnow)

    recordings = relationship('Recordings')
    session = relationship('Sessions')


class Transcriptions(Base):
    __tablename__ = 'transcriptions'

    id = Column(Integer, primary_key=True)
    recording_id = Column(ForeignKey('recordings.id'), nullable=False)
    session_id = Column(ForeignKey('sessions.id'), nullable=False)
    text = Column(Text, nullable=False)
    created = Column(DateTime, default=datetime.utcnow)

    recordings = relationship('Recordings')
    session = relationship('Sessions')


class EmotionAnalysis(Base):
    __tablename__ = 'emotion_analysis'

    id = Column(Integer, primary_key=True)
    recording_id = Column(ForeignKey('recordings.id'), nullable=False)
    session_id = Column(ForeignKey('sessions.id'), nullable=False)
    emotion = Column(ENUM(Emotion), nullable=False)
    confidence = (Float, CheckConstraint('confidence >= 0 and confidence <= 1'))
    created = Column(DateTime, default=datetime.utcnow)

    recordings = relationship('Recordings')
    session = relationship('Sessions')


class VoicePeaks(Base):
    __tablename__ = 'voice_peaks'

    id = Column(Integer, primary_key=True)
    recording_id = Column(ForeignKey('recordings.id'), nullable=False)
    session_id = Column(ForeignKey('sessions.id'), nullable=False)
    start_time = Column(String(50), nullable=False)
    end_time = Column(String(50), nullable=False)
    label = Column(String(50), nullable=False)
    confidence = (Float, CheckConstraint('confidence >= 0 and confidence <= 1'))
    created = Column(DateTime, default=datetime.utcnow)

    recordings = relationship('Recordings')
    session = relationship('Sessions')


class WordAssociations(Base):
    __tablename__ = 'word_associations'

    id = Column(Integer, primary_key=True)
    recording_id = Column(ForeignKey('recordings.id'), nullable=False)
    session_id = Column(ForeignKey('sessions.id'), nullable=False)
    word = Column(String(50), nullable=False)
    association = Column(String(50), nullable=False)
    confidence = (Float, CheckConstraint('confidence >= 0 and confidence <= 1'))
    created = Column(DateTime, default=datetime.utcnow)

    recordings = relationship('Recordings')
    session = relationship('Sessions')


class MlModels(Base):
    __tablename__ = 'ml_models'

    id = Column(Integer, primary_key=True)
    model = Column(ENUM(MachineLearningModel), nullable=False)
    word_associations_id = Column(ForeignKey('word_associations.id'), nullable=False)
    recording_id = Column(ForeignKey('recordings.id'), nullable=False)
    peak_id = Column(ForeignKey('voice_peaks.id'), nullable=False)
    sentiment_id = Column(ForeignKey('emotion_analysis.id'), nullable=False)
    transcription_id = Column(ForeignKey('transcriptions.id'), nullable=False)
    annotation_id = Column(ForeignKey('annotations.id'), nullable=False)
    created = Column(DateTime, default=datetime.utcnow)

    word_associations = relationship('WordAssociations')
    recordings = relationship('Recordings')
    voice_peaks = relationship('VoicePeaks')
    emotion_analysis = relationship('EmotionAnalysis')


