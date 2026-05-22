import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonicModule } from '@ionic/angular';

import { ActivatedRoute, Router } from '@angular/router';

import { OrdenService } from '../../services/orden.service';

@Component({
  selector: 'app-editar-orden',
  templateUrl: './editar-orden.page.html',
  styleUrls: ['./editar-orden.page.scss'],
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    IonicModule
  ]
})
export class EditarOrdenPage implements OnInit {

  id!: number;

  orden: any = {
    cliente: '',
    descripcion: ''
  };

  constructor(
    private route: ActivatedRoute,
    private ordenService: OrdenService,
    private router: Router
  ) {}

  ngOnInit() {

    this.id = Number(
      this.route.snapshot.paramMap.get('id')
    );

    this.ordenService
      .getOrdenById(this.id)
      .subscribe((res) => {

        this.orden = res;

      });

  }

  editarOrden() {

    this.ordenService
      .editarOrden(this.id, this.orden)
      .subscribe({

        next: () => {

          alert('Orden actualizada');

          this.router.navigate(['/ordenes']);

        },



        error: (err) => {

          console.error(err);

        }

      });

  }

}