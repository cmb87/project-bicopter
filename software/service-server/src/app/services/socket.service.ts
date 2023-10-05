import { Injectable } from '@angular/core';
import { environment } from './../../environments/environment';

import * as io from 'socket.io-client';

@Injectable({
  providedIn: 'root'
})
export class SocketService {
  public socket;

  constructor() {
    console.log("Socket service initialized")
    this.socket = io(environment.SOCKET_ENDPOINT, {reconnection: true, secure: true, rejectUnauthorized: false });
  }

  send(name: string, data: any) {
    this.socket.emit(name, data);
    console.log("Sending")
  }

  triggerStateChange(){
    this.socket.emit("statechange", "statechange")
  }
  
  changeURL(newURL: string) {
    console.log("Reconnecting to: "+newURL);
   // this.socket = io(newURL, {reconnection: true, secure: true, rejectUnauthorized: false });
    this.socket.io.uri = newURL ;
    console.log("Socket has been recreated!");
  }


}
