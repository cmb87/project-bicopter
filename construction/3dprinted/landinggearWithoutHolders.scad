t = 5;

rx = 100;
rdy = 4.1;
roy = 30;
royl = 50;





module rails(oz=2) {
    
  translate([-rx/2,roy/2,oz]) cube([rx,rdy,rdy]);
  mirror([0,1,0]){
    translate([-rx/2,roy/2,oz]) cube([rx,rdy,rdy]);
  }
    
}

module railsLow(oz=2) {
    
  translate([-rx/2,royl/2,oz]) cube([rx,rdy,rdy]);
  mirror([0,1,0]){
    translate([-rx/2,royl/2,oz]) cube([rx,rdy,rdy]);
  }
    
}


difference(){
union(){
  rotate([180,0,90])import("landingGearRaw.stl");
    
  hull(){
    translate([-15/2,27,4])rotate([0,90,0])cylinder(r=5,h=15,$fn=30);
    translate([-15/2,27-13/2,-3])cube([15,13,1]);
  }
  hull(){
    translate([-15/2,-27,4])rotate([0,90,0])cylinder(r=5,h=15,$fn=30);
    translate([-15/2,-27-13/2,-3])cube([15,13,1]);
  }
  

}


railsLow(oz=2);

}


