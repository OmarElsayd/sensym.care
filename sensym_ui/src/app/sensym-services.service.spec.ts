import { TestBed } from '@angular/core/testing';

import { SensymServicesService } from './sensym-services.service';

describe('SensymServicesService', () => {
  let service: SensymServicesService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SensymServicesService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
