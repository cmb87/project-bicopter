import { Component, OnInit, ViewChild, ElementRef, Input } from '@angular/core';

import { SocketService } from "../../services/socket.service";


@Component({
  selector: 'app-videofeed',
  templateUrl: './videofeed.component.html',
  styleUrls: ['./videofeed.component.css']
})
export class VideofeedComponent implements OnInit {

  @ViewChild('canvas', {static: true})
  private canvas: ElementRef<HTMLCanvasElement>;
  private ctx: CanvasRenderingContext2D;
  private image = new Image();

  public inferenceRes = {};

  @Input()
  public socketiotopic: string = 'videofeed1'

  @Input()
  private imgsize = [300,300];

  constructor(private socketService: SocketService) { }

  ngOnInit(): void {

    // Canvas Polygon and Image
    this.ctx = this.canvas.nativeElement.getContext('2d');

    // Load background image for canvas
    this.image.onload = ()=> {
      this.ctx.drawImage(this.image, 0, 0, this.imgsize[0], this.imgsize[1]);
    }
    this.image.src = "../assets/imgs/dummy.png";

    // Define SocketIO Endpoint
    this.socketService.socket.on(this.socketiotopic, (data: any) => {
      this.image.src = data.frame;
      this._reloadImage();

      this.inferenceRes = JSON.parse(data.inferenceres);

      console.log(this.inferenceRes);
    });

  }

  private _reloadImage() {
    this.image.onload = () => {
      this.ctx.drawImage(this.image, 0, 0, this.imgsize[0], this.imgsize[1]);
    }
  }



}
