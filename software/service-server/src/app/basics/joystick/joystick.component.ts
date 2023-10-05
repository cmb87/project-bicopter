import { Component, OnInit, ViewChild, Input } from '@angular/core';
import { JoystickEvent, NgxJoystickComponent } from 'ngx-joystick';
import { JoystickManagerOptions, JoystickOutputData } from 'nipplejs';

import { SocketService } from "../../services/socket.service";

@Component({
  selector: 'app-joystick',
  templateUrl: './joystick.component.html',
  styleUrls: ['./joystick.component.css']
})
export class JoystickComponent implements OnInit {
  @ViewChild('staticJoystick') staticJoystick: NgxJoystickComponent;

  @Input()
  posy: string;
  
  @Input()
  socketiotopic: string = "j1";


  staticOptions: JoystickManagerOptions;
  staticOutputData: JoystickOutputData;
  directionStatic: string;
  interactingStatic: boolean;

  constructor(private socketService: SocketService) { }

  ngOnInit(): void {

    this.staticOptions = {
      mode: 'static',
      position: { left: this.posy, top: '50%' },
      color: 'blue',
    };

   }

  private _convertJoystick(p: number): number {
    return Math.round(1000+1000*(p+50)/100);
  }

  onStartStatic(event: JoystickEvent) {
    this.interactingStatic = true;
    //console.log("onStartStatic");

  }

  onEndStatic(event: JoystickEvent) {
    this.interactingStatic = false;
    console.log("onEndStatic"); 
    var px = this._convertJoystick(0);
    var py = this._convertJoystick(0);
    console.log(this.socketiotopic, px, py);

    this.socketService.send(this.socketiotopic, [px, py])

  }

  onMoveStatic(event: JoystickEvent) {
    this.staticOutputData = event.data;
    var px = this._convertJoystick(event.data.instance.frontPosition.x);
    var py = this._convertJoystick(event.data.instance.frontPosition.y);
    console.log(this.socketiotopic, px, py);

    this.socketService.send(this.socketiotopic, [px, py])
  }

  onPlainUpStatic(event: JoystickEvent) {
    this.directionStatic = 'UP';
    //console.log("onPlainUpStatic");
  }

  onPlainDownStatic(event: JoystickEvent) {
    this.directionStatic = 'DOWN';
    //console.log("onPlainDownStatic");
  }

  onPlainLeftStatic(event: JoystickEvent) {
    this.directionStatic = 'LEFT';
    //console.log("onPlainLeftStatic");
  }

  onPlainRightStatic(event: JoystickEvent) {
    this.directionStatic = 'RIGHT';
    //console.log("onPlainRightStatic");
  }

}
