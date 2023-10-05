import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-analytics',
  templateUrl: './analytics.component.html',
  styleUrls: ['./analytics.component.css']
})
export class AnalyticsComponent implements OnInit {

  public videofeed1topic: string ="videofeed1";
  public videofeed2topic: string ="videofeed2";
  public videofeed3topic: string ="videofeed3";

  public slider1topic: string = "throttle";
  public slider2topic: string = "yaw";
  public joysticktopic: string = "joystick";

  // Monitoring control commands from joystick
  public controltopic: string = "control";

  constructor() { }

  ngOnInit(): void {}



}
