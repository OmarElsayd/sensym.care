import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { baseUrl } from 'src/environments/environment.development';
import { catchError, map, Observable, throwError } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class LoginServiceService {

  constructor(private http: HttpClient) { }
    
  login(data: any):Observable<any>{
    return this.http.put(`${baseUrl}/voice_analysis/start_session`, data)
    .pipe(
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
