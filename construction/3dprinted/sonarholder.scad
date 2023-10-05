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
  translate([-25/2,-60/2,-3])cube([25,60,3]);
  translate([-25/2 + 6,-10/2,-6])cube([15,10,6]);
    
  hull(){
    translate([-25/2,27,4])rotate([0,90,0])cylinder(r=5,h=25,$fn=30);
    translate([-25/2,27-13/2,-3])cube([25,13,1]);
  }
  hull(){
    translate([-25/2,-27,4])rotate([0,90,0])cylinder(r=5,h=25,$fn=30);
    translate([-25/2,-27-13/2,-3])cube([25,13,1]);
  }
  

}

  
  translate([0,26/2,-7])cylinder(r=17/2,h=10,$fn=30);

  translate([0,-26/2,-7])cylinder(r=17/2,h=10,$fn=30);
railsLow(oz=2);
railsLow(oz=5);
}

