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
  translate([-15/2,-40/2,-3])cube([15,40,3]);
    
  hull(){
    translate([-15/2,27-10,4])rotate([0,90,0])cylinder(r=4,h=15,$fn=30);
    translate([-15/2,27-8/2-10,-3])cube([15,8,1]);
  }
  hull(){
    translate([-15/2,-27+10,4])rotate([0,90,0])cylinder(r=4,h=15,$fn=30);
    translate([-15/2,-27-8/2+10,-3])cube([15,8,1]);
  }
  
}




rails(oz=0);

}


