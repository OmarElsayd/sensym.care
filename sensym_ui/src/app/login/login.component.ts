import { Component } from '@angular/core';
import { LoginServiceService } from 'src/app/login/login-service.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent {
  title = 'SENSYM.CARE';
  version = '1.0.0';
  date = new Date().toLocaleDateString();
  time = new Date().toLocaleTimeString();
  first_name!: string;
  last_name!: string;


  constructor(private loginService: LoginServiceService) {  }

  start_session() {
    console.log(this.first_name);
    console.log(this.last_name);
    this.loginService.login({first_name: this.first_name,last_name: this.last_name}).subscribe((data: any) => {
      console.log(data);
      window.location.href = '/voice-engine';

      if (localStorage.getItem('first_name') != null) {
        localStorage.removeItem('first_name');
      }
      if (localStorage.getItem('last_name') != null) {
        localStorage.removeItem('last_name');
      }
      if (localStorage.getItem('user_id') != null) {
        localStorage.removeItem('user_id');
      }
      if (localStorage.getItem('session_id') != null) {
        localStorage.removeItem('session_id');
      }

      localStorage.setItem('user_id', data.user_id);
      localStorage.setItem('session_id', data.session_id);
      localStorage.setItem('first_name', this.first_name);
      localStorage.setItem('last_name', this.last_name);
    });

  }

}
