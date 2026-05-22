import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonicModule, ToastController } from '@ionic/angular';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-crear-orden',
  templateUrl: './crear-orden.page.html',
  styleUrls: ['./crear-orden.page.scss'],
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    IonicModule
  ]
})
export class CrearOrdenPage implements OnInit {

  private apiUrl = 'http://127.0.0.1:5000/api';

  clientes: any[] = [];
  empleados: any[] = [];
  equipos: any[] = [];
  servicios: any[] = [];

  orden = {
    fecha_solicitud: '',
    estado: 'Pendiente',
    id_cliente: '',
    id_empleado: '',
    id_equipo: '',
    id_servicio: '',
    fecha_inicio: '',
    fecha_fin: '',
    resultado: ''
  };

  constructor(
    private http: HttpClient,
    private router: Router,
    private toastController: ToastController
  ) {}

  ngOnInit() {

    this.cargarClientes();
    this.cargarEmpleados();
    this.cargarEquipos();
    this.cargarServicios();

  }

  cargarClientes() {

    this.http.get<any[]>(`${this.apiUrl}/clientes`)
      .subscribe({

        next: (res) => {
          this.clientes = res;
        },

        error: (err) => {
          console.error(err);
        }

      });

  }

  cargarEmpleados() {

    this.http.get<any[]>(`${this.apiUrl}/empleados`)
      .subscribe({

        next: (res) => {
          this.empleados = res;
        },

        error: (err) => {
          console.error(err);
        }

      });

  }

  cargarEquipos() {

    this.http.get<any[]>(`${this.apiUrl}/equipos`)
      .subscribe({

        next: (res) => {
          this.equipos = res;
        },

        error: (err) => {
          console.error(err);
        }

      });

  }

  cargarServicios() {

    this.http.get<any[]>(`${this.apiUrl}/servicios`)
      .subscribe({

        next: (res) => {
          this.servicios = res;
        },

        error: (err) => {
          console.error(err);
        }

      });

  }

  guardarOrden() {

    this.http.post(
      `${this.apiUrl}/ordenes`,
      this.orden
    ).subscribe({

      next: async () => {

        const toast = await this.toastController.create({
          message: 'Orden creada correctamente',
          duration: 2000,
          color: 'success'
        });

        await toast.present();

        this.router.navigate(['/ordenes']);

      },

      error: async (err) => {

        console.error(err);

        const toast = await this.toastController.create({
          message: 'Error al guardar',
          duration: 2000,
          color: 'danger'
        });

        await toast.present();

      },
      
      

    });

  }

}