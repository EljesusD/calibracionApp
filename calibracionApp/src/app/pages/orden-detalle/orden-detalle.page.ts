import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IonicModule } from '@ionic/angular';

import { ActivatedRoute } from '@angular/router';

import { OrdenService } from '../../services/orden.service';

@Component({
  selector: 'app-orden-detalle',
  templateUrl: './orden-detalle.page.html',
  styleUrls: ['./orden-detalle.page.scss'],
  standalone: true,
  imports: [CommonModule, IonicModule]
})
export class OrdenDetallePage implements OnInit {
editar(arg0: any) {
throw new Error('Method not implemented.');
}

  detalles: any[] = [];

  idOrden: number = 0;

  constructor(
    private route: ActivatedRoute,
    private ordenService: OrdenService
  ) {}

  ngOnInit() {

    this.idOrden = Number(
      this.route.snapshot.paramMap.get('id')
    );

    console.log('ORDEN:', this.idOrden);

    this.ordenService
      .getDetalleOrden(this.idOrden)
      .subscribe({

        next: (res: any) => {

          console.log(res);

          this.detalles = res;

        },

        error: (err) => {

          console.error(err);

        }

      });

  }

}