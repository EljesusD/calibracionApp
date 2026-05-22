import { Component } from '@angular/core';
import { IonicModule } from '@ionic/angular';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

import { AuthService } from '../../services/auth';

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, FormsModule]
})
export class LoginPage {

  username = '';
  password = '';

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  login() {

    this.authService.login({

  username: this.username,
  password: this.password

}).subscribe({

  next: (res: any) => {

    console.log(res);

    if(res.status === 'ok'){

      this.router.navigate(['/home']);

    }

  },

  error: (err) => {

    console.error(err);

    alert('Credenciales incorrectas');

  }

});

}

}