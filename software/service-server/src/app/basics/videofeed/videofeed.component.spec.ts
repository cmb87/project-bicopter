import { ComponentFixture, TestBed } from '@angular/core/testing';

import { VideofeedComponent } from './videofeed.component';

describe('VideofeedComponent', () => {
  let component: VideofeedComponent;
  let fixture: ComponentFixture<VideofeedComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ VideofeedComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(VideofeedComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
