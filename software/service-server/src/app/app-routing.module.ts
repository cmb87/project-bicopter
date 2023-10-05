import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HomeComponent } from './components/home/home.component';
import { AboutComponent } from './components/about/about.component';
import { AnalyticsComponent } from './components/analytics/analytics.component';
import { SocketsettingsComponent } from './components/socketsettings/socketsettings.component'
//import { ExternalpageComponent } from './basics/externalpage/externalpage.component';

const routes: Routes = [
  {path:  "", pathMatch:  "full",redirectTo:  "home"},
  {path: "home", component: HomeComponent},
  {path: "analytics", component: AnalyticsComponent},
  {path: "about", component: AboutComponent},
  {path: "settings", component: SocketsettingsComponent}
//  {path: "external", component: ExternalpageComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
