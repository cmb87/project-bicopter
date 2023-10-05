t = 5;

rx = 100;
rdy = 4.1;
roy = 30;
royl = 50;

p0 = [0,0,18];
p1 = [0,25,18];
p2 = [40,15,18];
p3 = [40,0,18];

k = 12;


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


module span() {
difference(){
  hull(){
    translate([p0[0],p0[1],0])cylinder(r=p0[2]/2, h=t, $fn=20);
    translate([p1[0],p1[1],0])cylinder(r=p1[2]/2, h=t, $fn=20);
    translate([p2[0],p2[1],0])cylinder(r=p2[2]/2, h=t, $fn=20);
    translate([p3[0],p3[1],0])cylinder(r=p3[2]/2, h=t, $fn=20);

  }
  
  hull(){
    translate([p0[0]+3,p0[1]-3,-1])cylinder(r=p0[2]/k, h=2*t, $fn=20);
    translate([p1[0]+3,p1[1]-3,-1])cylinder(r=p1[2]/k, h=2*t, $fn=20);
    translate([p2[0]-3,p2[1]-3,-1])cylinder(r=p2[2]/k, h=2*t, $fn=20);
    translate([p3[0]-3,p3[1]-3,-1])cylinder(r=p3[2]/k, h=2*t, $fn=20);
  }

  translate([-120/2,-40,-1])cube([120,40,10]);
}
}

module spanComplete() {
    difference() {
    rotate([0,-90,0])
    union(){
      span();
      mirror([0,1,0])span();
    };

    translate([0,0,38])rails();
    translate([0,0,-5])railsLow();

    } 
}

module nose() {
    
  hull(){
  difference(){
    translate([0,0,0])spanComplete();
    translate([-6,-70/2,-30]) cube([12,70,60]);
  }
  
  
  translate([50,-20/2,30]) cube([3,20,3]);
  }
}

difference(){
union(){
  nose();
  spanComplete();
}
translate([-43,0,38])rails();
translate([20,0,18])cylinder(r=2,h=40,$fn=20);
translate([20,0,42])cylinder(r=4,h=40,$fn=20);
translate([-6,-30/2,29]) cube([38,30,8]);
}


