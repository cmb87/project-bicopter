import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StatechangebuttonComponent } from './statechangebutton.component';

describe('StatechangebuttonComponent', () => {
  let component: StatechangebuttonComponent;
  let fixture: ComponentFixture<StatechangebuttonComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ StatechangebuttonComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(StatechangebuttonComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
