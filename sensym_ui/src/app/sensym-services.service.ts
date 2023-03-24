import { HttpClient, HttpErrorResponse } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { catchError, map, throwError } from "rxjs";
import { baseUrl } from "src/environments/environment.development";

@Injectable({
  providedIn: 'root'
})
export class SensymServicesService {

  constructor(private httpClient: HttpClient) { }

  public sendEmtionsToAnalysis(emoDict: any, userInfo: any) {
    
    return this.httpClient.post(`${baseUrl}/voice_analysis/voice_recording_analysis_graph`, {
      emo_dict: emoDict, user_info: userInfo
    }).pipe(
      map(data => data),
      catchError(this.handleError)
    );
  }

  private handleError(error: HttpErrorResponse) {
    alert(error.error.detail);
    return throwError(
      'Something bad happened; please try again later.');
  };

}
