import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { VoiceEngineComponent } from './voice-engine/voice-engine.component';
import { LoginComponent } from './login/login.component';
import { HttpClientModule } from '@angular/common/http';
import { LoginServiceService } from './login/login-service.service';
import { FormsModule } from '@angular/forms'; 
import { MatFormFieldModule } from '@angular/material/form-field'; 
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { BrowserAnimationsModule } from 
    '@angular/platform-browser/animations';
import { AnalysisComponent } from './analysis/analysis.component';

@NgModule({
  declarations: [
    AppComponent,
    VoiceEngineComponent,
    LoginComponent,
    AnalysisComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule, // import HttpClientModule here
    FormsModule, // import FormsModule here
    MatFormFieldModule,
    BrowserAnimationsModule,
    MatCardModule,
    MatIconModule
  ],

  providers: [LoginServiceService],
  bootstrap: [AppComponent]
})
export class AppModule { }
