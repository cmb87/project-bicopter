import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ControlmonitorComponent } from './controlmonitor.component';

describe('ControlmonitorComponent', () => {
  let component: ControlmonitorComponent;
  let fixture: ComponentFixture<ControlmonitorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ControlmonitorComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ControlmonitorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
