
import { Component, OnInit } from '@angular/core';
import { VoiceEngineService } from './voice_engin_services/voice-engine.service';
import { SensymServicesService } from '../sensym-services.service';


@Component({
  selector: 'app-voice-engine',
  templateUrl: './voice-engine.component.html',
  styleUrls: ['./voice-engine.component.scss'],
  providers: [VoiceEngineService]
})
export class VoiceEngineComponent implements OnInit {
  title = 'SENSYM.CARE';
  version = '1.0.0';
  date = new Date().toLocaleDateString();
  time = new Date().toLocaleTimeString();

  user_info = {
    first_name: localStorage.getItem('first_name'),
    last_name: localStorage.getItem('last_name'),
    user_id: localStorage.getItem('user_id'),
    session_id: localStorage.getItem('session_id')
  }


  constructor(public VoiceEngine: VoiceEngineService, private SensymServicesService: SensymServicesService) { 
    this.VoiceEngine.init();
  }

  ngOnInit(): void {


  }

  start() {
    // this.VoiceEngine.startVoiceGraph();
    this.VoiceEngine.start();
    this.VoiceEngine.startRecording();
  }

  stop() {
    // this.VoiceEngine.stopVoiceGraph();
    this.VoiceEngine.stop();
    this.VoiceEngine.stopRecording();
  }
  clear() {
    this.VoiceEngine.transcript = '';
  }

  async sendTextForAnalysis() {
    if (this.VoiceEngine.transcript.length == 0) {
      alert('Please enter some text');
      return;
    }
    
    if (localStorage.getItem('textData') != null) {
      localStorage.removeItem('textData');
    }
    localStorage.setItem('textData', this.VoiceEngine.transcript);
  
    try {
      const data: any = await this.VoiceEngine.sendTextForAnalysis({text: this.VoiceEngine.transcript}).toPromise();
      if (localStorage.getItem('voiceAnalysisData') != null) {
        localStorage.removeItem('voiceAnalysisData');
      }
      localStorage.setItem('voiceAnalysisData', JSON.stringify(data));
    } catch (error) {
      console.error(error);
    }
  
    try {
      const response: any = await this.VoiceEngine.startRecordingAnlysis(this.user_info).toPromise();
      console.log('Data from startRecordingAnlysis:', response);
    } catch (error) {
      console.error(error);
    }
    
    let analysisData = JSON.parse(localStorage.getItem('voiceAnalysisData') || '{}');
    this.SensymServicesService.sendEmtionsToAnalysis(analysisData, this.user_info).subscribe(
      (response: any) => {
        console.log(response);
      },
      (error: any) => {
        console.log(error);
      }
    );

  
    this.VoiceEngine.transcript = '';
    window.location.href = '/analysis';
  }

}
