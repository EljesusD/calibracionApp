import { Component } from '@angular/core';
import {
  IonApp,
  IonRouterOutlet,
  IonMenu,
  IonHeader,
  IonToolbar,
  IonTitle,
  IonContent,
  IonList,
  IonItem,
  IonMenuToggle,
  IonIcon,
  IonLabel
} from '@ionic/angular/standalone';

import { RouterModule } from '@angular/router';

import {
  home,
  documentText,
  logOut
} from 'ionicons/icons';

import { addIcons } from 'ionicons';

@Component({
  selector: 'app-root',
  templateUrl: 'app.component.html',
  standalone: true,
  imports: [
    IonApp,
    IonRouterOutlet,
    IonMenu,
    IonHeader,
    IonToolbar,
    IonTitle,
    IonContent,
    IonList,
    IonItem,
    IonMenuToggle,
    IonIcon,
    IonLabel,
    RouterModule
  ],
})
export class AppComponent {

  constructor() {

    addIcons({
      home,
      documentText,
      logOut
    });

  }

}