import random
import string
from datetime import datetime

from sensym_models.voice_analysis_db.session import set_session
from sensym_models.voice_analysis_db.voice_db_models import Users, Sessions, Recordings, Role


def random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))


def create_user():
    session = set_session()
    with session.begin() as s:
        for i in range(1000):
            name = random_string(10)
            email = name + "@example.com"
            password = random_string(15)
            role = random.choice([Role.admin, Role.doctor, Role.client])
            user = Users(name=name, email=email, password=password, role=role)
            s.add(user)


def create_sessions():
    session = set_session()
    with session.begin() as s:
        users_count = s.query(Users).count()

        for i in range(1000):
            user_id = random.randint(1, users_count)
            session_created = datetime.utcnow()
            session = Sessions(user_id=user_id, created=session_created)
            s.add(session)


def create_recording():
    session = set_session()
    with session.begin() as s:
        users_count = s.query(Users).count()
        sessions_count = s.query(Sessions).count()

        for i in range(1000):
            user_id = random.randint(1, users_count)
            session_id = random.randint(1, sessions_count)
            recording_time = datetime.utcnow()
            recording_path = random_string(10)
            recording = Recordings(user_id=user_id, session_id=session_id, recording_time=recording_time, recording_path=recording_path)
            s.add(recording)


