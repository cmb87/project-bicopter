import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-control',
  templateUrl: './control.component.html',
  styleUrls: ['./control.component.css']
})
export class ControlComponent implements OnInit {
 
  public videofeed2topic: string ="videofeed2";
  public videofeed1topic: string ="videofeed1";
  public videofeed3topic: string ="videofeed3";

  public slider1topic: string = "throttle";
  public slider2topic: string = "yaw";
  public joysticktopic: string = "joystick";

  constructor() { }

  ngOnInit(): void {
  }

}
