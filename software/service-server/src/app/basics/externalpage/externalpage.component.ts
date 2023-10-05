import {Component, OnInit} from '@angular/core';
import { Location } from '@angular/common';
import { Router } from '@angular/router';

@Component({
    selector: 'app-external-page',
    templateUrl: './externalpage.component.html',
    styleUrls: ['./externalpage.component.css']
})

export class ExternalpageComponent implements OnInit {

    title = 'app works!';

    constructor(private router: Router, private loc: Location){};

    ngOnInit(): void {
    }

    dummy() {

        //this.router.navigate(['/','jenkins/'])
        const angularRoute = this.loc.path();
        const url = window.location.href;
      
        const domainAndApp = url.replace(angularRoute, '');
        console.log(domainAndApp);
        window.location.href=domainAndApp+"jenkins/";
    
      }

}