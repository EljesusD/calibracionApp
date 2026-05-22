import { ComponentFixture, TestBed } from '@angular/core/testing';
import { EditarOrdenPage } from './editar-orden.page';

describe('EditarOrdenPage', () => {
  let component: EditarOrdenPage;
  let fixture: ComponentFixture<EditarOrdenPage>;

  beforeEach(() => {
    fixture = TestBed.createComponent(EditarOrdenPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
