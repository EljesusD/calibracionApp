import { ComponentFixture, TestBed } from '@angular/core/testing';
import { OrdenDetallePage } from './orden-detalle.page';

describe('OrdenDetallePage', () => {
  let component: OrdenDetallePage;
  let fixture: ComponentFixture<OrdenDetallePage>;

  beforeEach(() => {
    fixture = TestBed.createComponent(OrdenDetallePage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
