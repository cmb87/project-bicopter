import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { FormsModule } from '@angular/forms';
import { NgxJoystickModule } from 'ngx-joystick';
import { NgxSliderModule } from '@angular-slider/ngx-slider';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import { NavbarComponent } from './basics/navbar/navbar.component';
import { ExternalpageComponent } from './basics/externalpage/externalpage.component';
import { HomeComponent } from './components/home/home.component';
import { JoystickComponent } from './basics/joystick/joystick.component';
import { StatechangebuttonComponent } from './basics/statechangebutton/statechangebutton.component';
import { SliderComponent } from './basics/slider/slider.component';
import { VideofeedComponent } from './basics/videofeed/videofeed.component';
import { ControlComponent } from './components/control/control.component';
import { FooterComponent } from './basics/footer/footer.component';
import { AboutComponent } from './components/about/about.component';
import { AnalyticsComponent } from './components/analytics/analytics.component';
import { ImageitemComponent } from './basics/imageitem/imageitem.component';
import { SocketsettingsComponent } from './components/socketsettings/socketsettings.component';
import { ControlmonitorComponent } from './basics/controlmonitor/controlmonitor.component';

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    ExternalpageComponent,
    HomeComponent,
    JoystickComponent,
    StatechangebuttonComponent,
    SliderComponent,
    VideofeedComponent,
    ControlComponent,
    FooterComponent,
    AboutComponent,
    AnalyticsComponent,
    ImageitemComponent,
    ControlmonitorComponent,
    SocketsettingsComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    AppRoutingModule,
    NgbModule,
    NgxJoystickModule,
    NgxSliderModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
