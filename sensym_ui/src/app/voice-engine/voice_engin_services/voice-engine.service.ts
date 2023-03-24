import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { baseUrl } from 'src/environments/environment.development';
import { catchError, map, Observable, Subject, throwError } from 'rxjs';

declare var webkitSpeechRecognition: any;

@Injectable({
  providedIn: 'root'
})
export class VoiceEngineService {
  recognition =  new webkitSpeechRecognition();
  isStoppedSpeechRecog = false;
  public text = '';
  public transcript = '';
  temp!: string;
  socket!: WebSocket;


  constructor(private httpClint: HttpClient) {
   }

  init() {
    this.recognition.interimResults = true;
    this.recognition.lang = 'en-US';

    this.recognition.addEventListener('result', (e: any) => {
      const transcript = Array.from(e.results)
        .map((result: any) => result[0])
        .map((result: any) => result.transcript)
        .join('');

      if (e.results[0].isFinal) {
        this.temp = transcript;
        this.text = this.temp;
        this.transcript = this.transcript + '. ' + this.text;
        console.log(this.transcript);
      }
    }
    );
  }

  start() {
    this.isStoppedSpeechRecog = false;
    this.recognition.start();
    this.recognition.addEventListener('end', (condition: any) => {
      if (this.isStoppedSpeechRecog) {
        this.recognition.stop();
      }else{
        this.wordConcat();
        this.recognition.start();
      }
    });

  }
  stop() {
    this.isStoppedSpeechRecog = true;
    this.wordConcat();
    this.recognition.stop();
  }
  wordConcat() {
    this.text = this.text + ' ' + this.temp + '.';
    this.temp = '';
  }

  sendTextForAnalysis(data: any):Observable<any> {
    return this.httpClint.post(`${baseUrl}/voice_analysis/voice_analysis`, data).pipe(
      map(data => data),
      catchError(this.handleError)
    );
  }
  startVoiceGraph() {
    this.socket = new WebSocket('ws://localhost:8000/voice_analysis/voice_graph');
    this.socket.onopen = () => {
      console.log('WebSocket connection opened');
    };
    this.socket.onmessage = (event) => {
      console.log('Received:', event.data);
    };
    this.socket.onclose = (event) => {
      console.log('WebSocket connection closed:', event.code, event.reason);
    };
  }
  stopVoiceGraph(): void {
    if (this.socket.readyState === WebSocket.OPEN) {
      this.socket.send('stop');
    } else {
      console.log("Trying to stop voice graph...");
      this.socket.addEventListener('open', () => {
        console.log("Socket is open, sending 'stop' message...");
        this.socket.send('stop');
      });
    }
  }
  
  startRecording() {
    const userInfo = {
      first_name: localStorage.getItem("first_name"),
      last_name: localStorage.getItem("last_name"),
      user_id: localStorage.getItem("user_id"),
      session_id: localStorage.getItem("session_id")
    };
    this.socket = new WebSocket('ws://localhost:8000/voice_analysis/voice_recording');
  
    this.socket.onopen = () => {
      console.log('WebSocket connection opened');
      this.socket.send(JSON.stringify(userInfo));
      // Send a JSON message after the connection is established
      const message = {
        type: 'start_recording',
      };
      this.socket.send(JSON.stringify(message));
    };
  
    this.socket.onmessage = (event) => {
      console.log('Received:', event.data);
    };
  
    this.socket.onclose = (event) => {
      console.log('WebSocket connection closed:', event.code, event.reason);
    };
  }


  stopRecording(): void {
    if (this.socket.readyState === WebSocket.OPEN) {
      this.socket.send('stop');
    } else {
      console.log("Trying to stop voice graph...");
      this.socket.addEventListener('open', () => {
        console.log("Socket is open, sending 'stop' message...");
        this.socket.send('stop');
      });
    }
  }

  private handleError(error: HttpErrorResponse) {
    alert(error.error.detail);
    return throwError(
      'Something bad happened; please try again later.');
  };

  startRecordingAnlysis(data: any):Observable<any> {
    return this.httpClint.post(`${baseUrl}/voice_analysis/voice_recording_analysis`, data).pipe(
      map(data => data),
      catchError(this.handleError)
    );
  }


}
