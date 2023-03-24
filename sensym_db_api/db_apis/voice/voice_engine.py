
import asyncio
import io
import logging
import os
from scipy import signal
import struct
import time as TIME
import wave
import numpy as np
import matplotlib
import scipy

from db_apis.voice.sentmint_ml import SentimentAnalyzer, convert_to_list, sentiments_histogram, sentiments_piechart, train_model
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from db_apis.voice.config import VoiceGraphConfig
from fastapi.responses import StreamingResponse
from db_apis.voice.session import get_db, session_transcation
import nltk
import pyaudio
from fastapi.exceptions import WebSocketRequestValidationError
from sensym_models.voice_analysis_db.session import set_session
from sensym_models.voice_analysis_db.voice_db_models import EmotionConfig, Sessions, Users

if not nltk.data.find('tokenizers/punkt'):
    nltk.download('punkt')
    nltk.download('vader_lexicon')
    nltk.download('stopwords')

from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from fastapi import APIRouter, Depends, HTTPException, WebSocket, status
from textblob import TextBlob
from pydantic import BaseModel
from sqlalchemy.orm import Session


logging.basicConfig(filename='mylog.txt', level=logging.INFO)
logger = logging.getLogger("FastAPI app Logging")

router = APIRouter(
    prefix="/voice_analysis",
    tags=["voice_analysis"],
    responses={404: {"description": "Not found"}},
)

def extract_sentiment_vader(text):
    sid = SentimentIntensityAnalyzer()
    scores = sid.polarity_scores(text)
    if scores['compound'] > 0:
        return 'positive'
    elif scores['compound'] < 0:
        return 'negative'
    else:
        return 'neutral'

def extract_sentiment_textblob(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    if sentiment > 0:
        return 'positive'
    elif sentiment < 0:
        return 'negative'
    else:
        return 'neutral'

def extract_emotions(text):
    words = word_tokenize(text.lower())
    session = set_session()

    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word.isalpha() and word not in stop_words]

    emotions = {}

    with session.begin() as s:
        lexicon = s.query(EmotionConfig).first().emotion_json_config

    for word in words:
        if word in lexicon:
            for emotion, value in lexicon[word].items():
                if emotion not in emotions:
                    emotions[emotion] = 0
                emotions[emotion] += value
    return emotions


class VoiceAnalysisinput(BaseModel):
    text: str

class VoiceAnalysisoutput(BaseModel):
    vader_sentiment: str
    textblob_sentiment: str
    emotions: dict

@router.post(
    "/voice_analysis",
    response_model=VoiceAnalysisoutput,
    status_code=status.HTTP_200_OK,
)
def sentiment(body: VoiceAnalysisinput):
    try:
        vader_sentiment = extract_sentiment_vader(body.text)
        textblob_sentiment = extract_sentiment_textblob(body.text)
        emotions = extract_emotions(body.text)
        return VoiceAnalysisoutput(
                vader_sentiment=vader_sentiment,
                textblob_sentiment=textblob_sentiment,
                emotions=emotions,
        )
    except HTTPException as e:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail= f"Internal server error {e}")
    
    
class UserInput(BaseModel):
    first_name: str
    last_name: str
    
    class Config:
        orm_mode = True


class StartSession(BaseModel):
    user_id: int
    session_id: int
    message: str

@router.put(
    "/start_session",
    response_model=StartSession,
    status_code=status.HTTP_200_OK
)
def create_session(body: UserInput, session: Session = Depends(get_db)):
    try:
        user_exists = session.query(Users).filter_by(first_name=body.first_name, last_name=body.last_name).first()
        if user_exists:
            new_session = Sessions(user_id=user_exists.id)
            session.add(new_session)
            session.commit()
        
            return StartSession(
                user_id=user_exists.id,
                session_id=new_session.id,
                message="Session started"
            )
        if not user_exists:
            with session_transcation(session) as session:
                new_user = Users(first_name=body.first_name, last_name=body.last_name)
                session.add(new_user)
                session.flush()    

                new_session = Sessions(user_id=new_user.id)  
                session.add(new_session)
                session.flush()
                    
                return StartSession(
                    user_id=new_user.id,
                    session_id=new_session.id,
                    message="Session started"
                )       
                
    except HTTPException as e:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail= f"Internal server error {e}")




@router.websocket("/voice_graph")
async def record_audio(websocket: WebSocket):
    try:
        await websocket.accept()  # send handshake message
        logger.info("WebSocket connection accepted")

        voice_config = VoiceGraphConfig()
        p = pyaudio.PyAudio()

        # start Recording
        stream = p.open(
            format=voice_config.FORMAT,
            channels=voice_config.CHANNELS,
            rate=voice_config.RATE,
            input=True,
            output=False,
            frames_per_buffer=voice_config.CHUNK,
        )
        logger.info("Recording started")

        fig, ax = plt.subplots()  # create a figure and a subplot
        x = np.arange(0, 2 * voice_config.CHUNK, 2)  # create an array containing the time
        line, = ax.plot(x, np.random.rand(voice_config.CHUNK))  # create a line object with random data

        ax.set_ylim(-16000, 16000)
        ax.set_xlim(0, voice_config.CHUNK)  # set the x axis limits
        fig.canvas.draw()  # draw the plot

        async def plot_generator():
            while True:
                try:
                    input_data = await asyncio.wait_for(websocket.receive_text(), timeout=0.001)
                    logger.info("WebSocket message received: %s", input_data)
                    if input_data == 'stop':
                        break
                    else:
                        await websocket.send_text('data')
                        logger.info("WebSocket message sent: data")
                except Exception as e:
                    logger.error("Error handling WebSocket message: %s", str(e))

                data = stream.read(voice_config.CHUNK)  # read a chunk of data
                data_int = struct.unpack(str(voice_config.CHUNK) + 'H', data)  # convert from bytes to int
                data_int = np.array(data_int, dtype='h')  # convert to numpy array
                wf_data = [i + 100 for i in data_int]  # add 100 to waveform data
                line.set_ydata(wf_data)  # update the data
                buf = io.BytesIO()
                fig.savefig(buf, format='png')
                buf.seek(0)
                yield buf.getvalue()

        response = StreamingResponse(plot_generator(), media_type="image/png")

    except HTTPException as e:
        raise
    except Exception as e:
        logger.exception("Internal server error: %s", str(e))
        raise HTTPException(status_code=500, detail=f"Internal server error {e}")

    plt.close(fig)
    await websocket.close()
    logger.info("WebSocket connection closed")
    
    
@router.get("/voice_graph")
async def get_voice_graph():
    return StreamingResponse(record_audio())




@router.websocket("/voice_recording")
async def recording_a_wav_file(websocket: WebSocket):
    """
    This method will record a wav file.
    Make sure that you are in the user work directory.
    :param websocket: The WebSocket instance
    :param first_name: The first name of the user
    :param last_name: The last name of the user
    :return: None
    """
    try:
        await websocket.accept()
        user_info = await websocket.receive_json()
        logger.info(user_info)
        logger.info(f"Recording started for user {user_info['first_name']} {user_info['last_name']} (user_id={user_info['user_id']}, session_id={user_info['session_id']})")

        voice_config = VoiceGraphConfig()
        chunk = voice_config.CHUNK
        sample_format = voice_config.FORMAT
        channels = voice_config.CHANNELS
        fs = voice_config.RATE
        
        path = "sensym_ui/src/assets"
        folder_name = f"{user_info['first_name']}_{user_info['last_name']}_{user_info['user_id']}"
        
        if folder_name not in os.listdir(path):
            os.mkdir(f"sensym_ui/src/assets/{folder_name}")

            
        filename = f"{path}/{folder_name}/{user_info['first_name']}_{user_info['last_name']}_{user_info['user_id']}_{user_info['session_id']}.wav"

        if os.path.exists(filename):
            logger.info(f"File {filename} already exists. Deleting it.")
            os.remove(filename)
        
        p = pyaudio.PyAudio()
        stream = p.open(format=sample_format,
                        channels=channels,
                        rate=fs,
                        frames_per_buffer=chunk,
                        input=True)

        frames = []
        while True:
            try:
                data = stream.read(chunk)
                frames.append(data)
                logger.debug(f"Recording {len(frames)} frames")
                message = await asyncio.wait_for(websocket.receive_text(), timeout=0.001)
                if message == "stop":
                    break
            except asyncio.exceptions.TimeoutError:
                continue

        stream.stop_stream()
        stream.close()
        p.terminate()

        logger.info(f"Recording stopped for user {user_info['first_name']} {user_info['last_name']} (user_id={user_info['user_id']}, session_id={user_info['session_id']})")
        wf = wave.open(filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close()
    except WebSocketRequestValidationError as e:
        logger.exception("Error handling WebSocket message: %s", str(e))
    except Exception as e:
        logger.exception("Internal server error: %s", str(e))
        raise HTTPException(status_code=500, detail=f"Internal server error {e}")


    
class UserInfo(BaseModel):
    first_name: str
    last_name: str
    user_id: str
    session_id: str
    
    
@router.post(
    "/voice_recording_analysis",
    status_code=status.HTTP_200_OK
    )
def voice_recording_analysis(
    user_info: UserInfo,
    ):
    """
    This method will analyze a wav file.
    :param file: The wav file
    :return: The analysis result
    """
    path = f"sensym_ui/src/assets/{user_info.first_name}_{user_info.last_name}_{user_info.user_id}"
    filename = f"{path}/{user_info.first_name}_{user_info.last_name}_{user_info.user_id}_{user_info.session_id}.wav"

    logger.info(f"Analyzing file {path}")

    if "audioRecording.png" in os.listdir(path):
        logger.info("File exists, removing audioRecording.png")
        os.remove(f"{path}/audioRecording.png")
    if "audioRecordingPeaks.png" in os.listdir(path):
        logger.info("File exists, removing audioRecordingPeaks.png")
        os.remove(f"{path}/audioRecordingPeaks.png")
        
    TIME.sleep(1)
    
    rate, data = scipy.io.wavfile.read(filename)
    duration = len(data) / rate
    time = np.linspace(0, duration, len(data), endpoint=False)
    
    plt.clf()
    plt.plot(time, data, color='green')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('Recording')
    plt.ylim((-2**15, 2**15))
    plt.savefig(f"{path}/audioRecording.png")
    
    plt.clf()
    peaks = signal.find_peaks(data, height=15000)[0]
    plt.plot(time, data)
    plt.plot(time[peaks], data[peaks], "x", color="red")
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('Recording Peaks detection')
    plt.savefig(f"{path}/audioRecordingPeaks.png")
    
    
@router.post(
    "/voice_recording_analysis_graph",
    status_code=status.HTTP_200_OK
    )
def plot_emotions(emo_dict: dict, user_info: UserInfo):
    logger.info(emo_dict)
    logger.info(user_info)
    
    try:
        path = f"sensym_ui/src/assets/{user_info.first_name}_{user_info.last_name}_{user_info.user_id}"
        
        if "emotions_analysis.png" in os.listdir(path):
            os.remove(f"{path}/emotions_analysis.png")

        data = emo_dict
        emotions = data["emotions"]

        # Prepare data for plotting
        emotion_names = list(emotions.keys())
        emotion_values = list(emotions.values())
        plt.clf()
        # Create a bar plot
        bars = plt.bar(emotion_names, emotion_values)
        # Calculate the midpoints of each bin
        x = [bar.get_x() + bar.get_width() / 2 for bar in bars]
        y = [bar.get_height() for bar in bars]

        # Draw a red line connecting the top of each bin
        plt.plot(x, y, color='red', linestyle='-', marker='o', markersize=4)

        # Set plot title and labels
        plt.title("Emotion Analysis")
        plt.ylabel("Scores")
        # Resize the graph    
        plt.subplots_adjust(left=0.15, bottom=0.18, right=0.9, top=0.9)

        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45)

        plt.savefig(f"{path}/emotions_analysis.png")
        
        return {"message": "Emotions analysis graph created"}
    except HTTPException as e:
        logger.exception("Error handling HTTP request: %s", str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error {e}")
    
    
    
def process_data(data):
    sentiment = data["vader_sentiment"]
    emotions = data["emotions"]

    if sentiment == "positive":
        print("The sentiment is positive.")
    elif sentiment == "negative":
        print("The sentiment is negative.")
    else:
        print("The sentiment is neutral.")

    most_common_emotion = max(emotions, key=emotions.get)
    print(f"The most common emotion is {most_common_emotion}.")



@router.put(
    "sentmint_ml_analysis",
    status_code=status.HTTP_200_OK,
)
def sentmints_ml(user_info: UserInfo, journal: VoiceAnalysisinput):
    
    if "sentiment_analysis.joblib" not in os.listdir("sensym_db_api/db_apis/voice"):
        train_model()
    try:
        sentiment_analyzer = SentimentAnalyzer("sensym_db_api/db_apis/voice/sentiment_dataset.csv")
        sentiment_analyzer.load_model("sensym_db_api/db_apis/voice/sentiment_analysis.joblib")

        path = f"sensym_ui/src/assets/{user_info.first_name}_{user_info.last_name}_{user_info.user_id}"
        
        accuracy = sentiment_analyzer.test()
        
        journal_sentences = convert_to_list(journal.text)
        journal_sentences = list(filter(None, journal_sentences))
        sentiments = sentiment_analyzer.predict(journal_sentences)
        
        sentiments_histogram(sentiments, path)
        sentiments_piechart(sentiments, path)
        
        
        return {
            "message": "Sentiment analysis graph created",
            "accuracy": accuracy
            }
    except HTTPException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error {e}")
        
        
