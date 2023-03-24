import json
import random
import string
from datetime import datetime

from sensym_models.voice_analysis_db.session import set_session
from sensym_models.voice_analysis_db.voice_db_models import Users, Sessions, Recordings, Role, EmotionConfig


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


def add_nrc_emotion():
    with open("python/scripts/NRC-Emotion-Lexicon-Wordlevel-v0.92.json", "r") as f:
        file = json.load(f)
    session = set_session()
        
    with session.begin() as s:
        
        config = EmotionConfig(emotion_json_config=file)
        s.add(config)
        s.commit()  
        
from transformers import pipeline, T5Tokenizer, T5ForConditionalGeneration, TextClassificationPipeline

def get_emotion(text):
    emotion_classifier = pipeline('text-classification', model='cardiffnlp/twitter-roberta-base-emotion')
    result = emotion_classifier(text)[0]
    return result['label'].split('_')[-1].lower()

# def get_sarcasm(text):
#     model_name = 'mrm8488/t5-base-finetuned-sarcasm-twitter'
#     tokenizer = T5Tokenizer.from_pretrained(model_name)
#     model = T5ForConditionalGeneration.from_pretrained(model_name)

#     inputs = tokenizer.encode("sarcasm: " + text, return_tensors="pt", max_length=512, truncation=True)
#     outputs = model.generate(inputs, max_length=128, num_return_sequences=1)
#     decoded_output = tokenizer.decode(outputs[0], skip_special_tokens=True)

#     sarcasm_label = decoded_output.strip()
#     return sarcasm_label

# text = "I just love it when my code doesn't work."

# emotion = get_emotion(text)
# sarcasm = get_sarcasm(text)

# print(f"Emotion: {emotion}")
# print(f"Sarcasm: {sarcasm}")
        
# add_nrc_emotion()   



import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D 


def lorenz(x, y, z, r, s=10, b=(8/3)):
    x_dot = s * (y - x)
    y_dot = r * x - y - x * z
    z_dot = x * y - b * z
    return x_dot, y_dot, z_dot

dt = 0.01
num_steps = 10000

xs = np.empty(num_steps + 1)
ys = np.empty(num_steps + 1)
zs = np.empty(num_steps + 1)


xs[0], ys[0], zs[0] = (11.8, 4.4, 2.4)

exit = input("Want to exit? ")

while exit == 'no':
    rval = int(input("Enter a value for r: "))
    for i in range(num_steps):
        x_dot, y_dot, z_dot = lorenz(xs[i], ys[i], zs[i], rval)
        xs[i + 1] = xs[i] + (x_dot * dt)
        ys[i + 1] = ys[i] + (y_dot * dt)
        zs[i + 1] = zs[i] + (z_dot * dt)

    fig = plt.figure()

    # 3D lorenz plot
    ax = fig.add_subplot(projection='3d')
    ax.plot(xs, ys, zs, lw=0.5)
    ax.set_xlabel("X Axis")
    ax.set_ylabel("Y Axis")
    ax.set_zlabel("Z Axis")
    ax.set_title("Lorenz Attractor")
    plt.show()

    # x plot
    plt.plot(xs)
    plt.xlabel("t")
    plt.ylabel("x - JPG")
    plt.title("x(t) [JPG] - r: " + str(rval))
    plt.show()

    # y plot
    plt.plot(ys)
    plt.xlabel("t")
    plt.ylabel("y - PNG")
    plt.title("y(t) [PNG] - r: " + str(rval))
    plt.show()

    # z plot
    plt.plot(zs)
    plt.xlabel("t")
    plt.ylabel("z - GIF")
    plt.title("z(t) [GIF] - r: " + str(rval))
    plt.show()

    exit = input("Do you want to exit? ")   

