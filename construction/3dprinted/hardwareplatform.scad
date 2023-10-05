t = 5;

rx = 100;
rdy = 4.1;
roy = 30;
royl = 50;





difference(){
union(){
  translate([-15/2,-62/2,-2])cube([15,62,2]);
    


  translate([0,+15,0])cylinder(r=5.5,h=4,$fn=30);
  translate([0,-15,0])cylinder(r=5.5,h=4,$fn=30);
    
  translate([-15/2,-1,-6])cube([15,2,6]);
  translate([0,31,-4])bracket();
  translate([0,-31,-4])mirror([0,1,0])bracket();
}

  translate([0,15,-5])cylinder(r=2.5,h=15,$fn=30);
  translate([0,15,-7])cylinder(r=4,h=10,$fn=30);
  translate([0,-15,-5])cylinder(r=2.5,h=15,$fn=30);
  translate([0,-15,-7])cylinder(r=4,h=10,$fn=30);



}

module bracket(){
  difference(){
    translate([-7.5,0,0])rotate([0,90,0])cylinder(r=4,h=15,$fn=6);
    translate([-15,-20,-10])cube([30,20,20]);
  }
}