from sqlalchemy.orm import sessionmaker

from sensym_models.voice_analysis_db.db_engine import create_db_engine


def set_session() -> sessionmaker:
    """
    Create a session to the database
    :return:    sessionmaker
    """
    engine = create_db_engine()
    session = sessionmaker(bind=engine)
    return session

engine = create_db_engine()
LocalSession = sessionmaker(bind=engine)



