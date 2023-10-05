import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ImageitemComponent } from './imageitem.component';

describe('ImageitemComponent', () => {
  let component: ImageitemComponent;
  let fixture: ComponentFixture<ImageitemComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ImageitemComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ImageitemComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
