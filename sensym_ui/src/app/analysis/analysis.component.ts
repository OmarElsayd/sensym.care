import { Component, ElementRef, OnInit, Renderer2, AfterViewInit } from '@angular/core';
import { SensymServicesService } from '../sensym-services.service';

@Component({
  selector: 'app-analysis',
  templateUrl: './analysis.component.html',
  styleUrls: ['./analysis.component.scss']
})
export class AnalysisComponent implements OnInit, AfterViewInit {
  title = 'SENSYM.CARE';
  version = '1.0.0';
  date = new Date().toLocaleDateString();
  time = new Date().toLocaleTimeString();
  PeaksPng = `assets/${localStorage.getItem('first_name')}_${localStorage.getItem('last_name')}_${localStorage.getItem("user_id")}/audioRecordingPeaks.png`;
  RecPng = `assets/${localStorage.getItem('first_name')}_${localStorage.getItem('last_name')}_${localStorage.getItem("user_id")}/audioRecording.png`;
  emotionPng = `assets/${localStorage.getItem('first_name')}_${localStorage.getItem('last_name')}_${localStorage.getItem("user_id")}/emotions_analysis.png`;
  recordingWave = `assets/${localStorage.getItem('first_name')}_${localStorage.getItem('last_name')}_${localStorage.getItem("user_id")}/${localStorage.getItem("first_name")}_${localStorage.getItem("last_name")}_${localStorage.getItem("user_id")}_${localStorage.getItem("session_id")}.wav`;
  analysisLabel: ElementRef;
  transcriptLabel: ElementRef;
  analysisLabelRef: ElementRef | undefined;
  transcriptLabelRef: ElementRef | undefined;
  analysis: string = '';
  transcript: string = '';

  constructor(private SensymServicesService: SensymServicesService, private renderer: Renderer2) {
    this.analysisLabel = new ElementRef(null);
    this.transcriptLabel = new ElementRef(null);
  }

  ngOnInit(): void {
    this.analysis = JSON.parse(localStorage.getItem('voiceAnalysisData') || '{}');
    this.transcript = localStorage.getItem('textData') || '';

    console.log(this.analysis); // Check if this.analysis is being updated correctly
    console.log(this.transcript); // Check if this.transcript is being updated correctly
  }

  ngAfterViewInit(): void {
    const analysisLabel = document.getElementById('analysis-label');
    if (analysisLabel) {
      analysisLabel.textContent = JSON.stringify(this.analysis, null, 4);
      
    }

    const transcriptLabel = document.getElementById('transcript-label');
    if (transcriptLabel) {
      transcriptLabel.textContent = this.transcript;
    }
  }

}
