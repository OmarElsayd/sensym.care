import pyaudio
from fastapi import FastAPI
from fastapi import WebSocket
from db_apis.voice import voice_engine
from fastapi.middleware.cors import CORSMiddleware

# from voice import voice_engine

app = FastAPI(
    title="Sensym DB API",
    description="Sensym DB API",
    version="1.0.0",
)

app.include_router(voice_engine.router)


# add middleware to set CORS headers
origins = [
    "http://localhost",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)