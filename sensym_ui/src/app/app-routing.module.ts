import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { VoiceEngineComponent } from './voice-engine/voice-engine.component';
import { LoginComponent } from './login/login.component';
import { AnalysisComponent } from './analysis/analysis.component';


const routes: Routes = [
  { path: 'voice-engine', component: VoiceEngineComponent },
  { path: '', component: LoginComponent },
  { path: 'analysis', component: AnalysisComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
