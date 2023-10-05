import { Component, OnInit } from '@angular/core';
import { SocketService } from "../../services/socket.service";

@Component({
  selector: 'app-statechangebutton',
  templateUrl: './statechangebutton.component.html',
  styleUrls: ['./statechangebutton.component.css']
})
export class StatechangebuttonComponent implements OnInit {

  constructor(private socketService: SocketService) { }

  ngOnInit(): void {
  }


  triggerStateChange():void {
    this.socketService.triggerStateChange();
  }
}
