import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class OrdenService {

  private apiUrl = 'http://192.168.8.4:5000/api';

  constructor(private http: HttpClient) {}

  getOrdenes(): Observable<any> {
    return this.http.get(`${this.apiUrl}/ordenes`);
  }

  getOrdenById(id: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/orden/${id}`);
  }

  getDetalleOrden(id: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/orden/${id}/detalle`);
  }

  crearOrden(orden: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/orden`, orden);
  }

  editarOrden(id: number, orden: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/orden/${id}`, orden);
  }

 eliminarOrden(id: number) {
  return this.http.put(
    `${this.apiUrl}/orden/${id}/eliminar`,
    {}
  );
}

}