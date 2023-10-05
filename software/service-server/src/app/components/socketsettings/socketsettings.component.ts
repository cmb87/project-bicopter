import { Component, OnInit, Input } from '@angular/core';
import { SocketService } from '../../services/socket.service';
import { environment } from './../../../environments/environment';

@Component({
  selector: 'app-socketsettings',
  templateUrl: './socketsettings.component.html',
  styleUrls: ['./socketsettings.component.css']
})
export class SocketsettingsComponent implements OnInit {

  @Input()
  public socketURL: string = environment.SOCKET_ENDPOINT;
  
  constructor(private socketService: SocketService) { }

  ngOnInit(): void {
  }

  changeURL(): void {
    this.socketService.changeURL(this.socketURL);
  }


}
