import { TestBed } from '@angular/core/testing';

import { Orden } from './orden.service';

describe('Orden', () => {
  let service: Orden;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Orden);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
