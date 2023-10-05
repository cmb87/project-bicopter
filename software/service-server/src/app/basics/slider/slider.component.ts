import { Component, OnInit, Input } from '@angular/core';
import { Options, ChangeContext } from '@angular-slider/ngx-slider';

import { SocketService } from "../../services/socket.service";

@Component({
  selector: 'app-slider',
  templateUrl: './slider.component.html',
  styleUrls: ['./slider.component.css']
})
export class SliderComponent implements OnInit {
  @Input()
  socketiotopic: string = "slider";
  
  value: number = 0;
  options: Options = {
    floor: 0,
    ceil: 100,
    vertical: false,
    getPointerColor: (value: number): string => {
      if (value <= 30) {
          return 'blue';
      }
      if (value <= 70) {
          return 'blue';
      }
      if (value <= 100) {
          return 'blue';
      }
      return '#2AE02A';
      }
  };

  constructor(private socketService: SocketService) { }

  ngOnInit(): void {
  }

  private _convertSlider(p: number): number {
    return Math.round(1000+1000*(p+0)/100);
  }

  onUserChangeEnd(changeContext: ChangeContext): void {
    var px = this._convertSlider(changeContext.value);
    this.socketService.send(this.socketiotopic, [px]);
  }


}
