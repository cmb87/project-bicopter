import { Component, OnInit, ViewChild, ElementRef, Input } from '@angular/core';
import { SocketService } from "../../services/socket.service";

@Component({
  selector: 'app-controlmonitor',
  templateUrl: './controlmonitor.component.html',
  styleUrls: ['./controlmonitor.component.css']
})
export class ControlmonitorComponent implements OnInit {

  @Input()
  public socketiotopic: string = 'control'

  public commands

  constructor(private socketService: SocketService) { }

  ngOnInit(): void {

    // Define SocketIO Endpoint
    this.socketService.socket.on(this.socketiotopic, (data: any) => {
      this.commands = {controller: data};
    });

  }

}
