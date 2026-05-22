import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IonicModule } from '@ionic/angular';
import { RouterModule, Router } from '@angular/router';

import { OrdenService } from '../../services/orden.service';

@Component({
  selector: 'app-ordenes',
  templateUrl: './ordenes.page.html',
  styleUrls: ['./ordenes.page.scss'],
  standalone: true,
  imports: [CommonModule, IonicModule, RouterModule]
})
export class OrdenesPage implements OnInit {

  ordenes: any[] = [];

  constructor(
    private ordenService: OrdenService,
    private router: Router
  ) {}

  ngOnInit() {

    console.log('Página órdenes cargada');

    this.ordenService.getOrdenes().subscribe({
      next: (res: any) => {
        console.log('datos',res);
        this.ordenes = res;
      },
      error: (err) => {
        console.error(err);
      }
    });
  }

  verDetalle(id: number) {
    this.router.navigate(['/orden', id]);
  }

  editar(id: number) {
    this.router.navigate(['/editar-orden', id]);
  }

eliminar(id: number) {

  const confirmar = confirm('¿Desea eliminar esta orden?');

  if(confirmar){

    this.ordenService.eliminarOrden(id).subscribe({

      next: () => {

        alert('Orden eliminada');

        this.ordenes = this.ordenes.filter(
          o => o.id !== id
        );

      },

      error: (err) => {
        console.error(err);
        alert('Error al eliminar');
      }

    });

  

  }

}
}
