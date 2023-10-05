import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SocketsettingsComponent } from './socketsettings.component';

describe('SocketsettingsComponent', () => {
  let component: SocketsettingsComponent;
  let fixture: ComponentFixture<SocketsettingsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SocketsettingsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SocketsettingsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
