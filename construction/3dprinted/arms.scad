difference(){

union(){
  difference(){
    rotate([90,0,0])rotate([0,-90,0])import("TRI_TAIL_V3.stl");
    translate([-5,-40/2,-1])cube([43,40,20]);
  }
  hull(){
    translate([15,-10/2,4])cube([2,10,10]);
    translate([38,-19.3/2,0])cube([2,19.3,15.5]);
  }


}

translate([20,0,-5])cylinder(r=0.6,h=40, $fn=20);
translate([30,0,-5])cylinder(r=0.6,h=40, $fn=20);
translate([10,-8.1/2,5])cube([32,8.1,8.2]);

}

