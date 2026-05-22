import { Routes } from '@angular/router';

export const routes: Routes = [

  // LOGIN
  {
    path: 'login',
    loadComponent: () =>
      import('./pages/login/login.page')
        .then(m => m.LoginPage),
  },

  // HOME
  {
    path: 'home',
    loadComponent: () =>
      import('./home/home.page')
        .then(m => m.HomePage),
  },

  // ORDENES
  {
    path: 'ordenes',
    loadComponent: () =>
      import('./pages/ordenes/ordenes.page')
        .then(m => m.OrdenesPage),
  },

  // DETALLE ORDEN
  {
    path: 'orden/:id',
    loadComponent: () =>
      import('./pages/orden-detalle/orden-detalle.page')
        .then(m => m.OrdenDetallePage),
  },

  // CREAR ORDEN
  {
    path: 'crear-orden',
    loadComponent: () =>
      import('./pages/crear-orden/crear-orden.page')
        .then(m => m.CrearOrdenPage),
  },

  // EDITAR ORDEN
  {
    path: 'editar-orden/:id',
    loadComponent: () =>
      import('./pages/editar-orden/editar-orden.page')
        .then(m => m.EditarOrdenPage),
  },

  // REDIRECCION INICIAL
  {
    path: '',
    redirectTo: 'login',
    pathMatch: 'full',
  },

];