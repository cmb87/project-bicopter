import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';

@Component({
  selector: 'app-imageitem',
  templateUrl: './imageitem.component.html',
  styleUrls: ['./imageitem.component.css']
})
export class ImageitemComponent implements OnInit {

  constructor() { }

  @ViewChild('canvas', {static: true})
  private canvas: ElementRef<HTMLCanvasElement>;
  private ctx: CanvasRenderingContext2D;
  private image = new Image();

  ngOnInit(): void {
  }

}
