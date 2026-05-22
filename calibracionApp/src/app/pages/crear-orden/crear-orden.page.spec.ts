import { ComponentFixture, TestBed } from '@angular/core/testing';
import { CrearOrdenPage } from './crear-orden.page';

describe('CrearOrdenPage', () => {
  let component: CrearOrdenPage;
  let fixture: ComponentFixture<CrearOrdenPage>;

  beforeEach(() => {
    fixture = TestBed.createComponent(CrearOrdenPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
