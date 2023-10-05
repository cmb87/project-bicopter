import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ExternalpageComponent } from './externalpage.component';

describe('ExternalpageComponent', () => {
  let component: ExternalpageComponent;
  let fixture: ComponentFixture<ExternalpageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ExternalpageComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ExternalpageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
