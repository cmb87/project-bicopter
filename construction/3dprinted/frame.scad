bw=40;
bh=60;

rx = 100;
rdy = 4.1;
roy = 30;

abx = 40;
adx0 = 8.1;
adx1 = 12;
ady = 30;
aoy = 8;
aoz = 3;
arot = 10;

acx = 23;
acy = 38;
acz = 10;


module rails(oz=2) {
    
  translate([-rx/2,roy/2,oz]) cube([rx,rdy,rdy]);
  mirror([0,1,0]){
    translate([-rx/2,roy/2,oz]) cube([rx,rdy,rdy]);
  }
    
}


difference(){
hull(){
  translate([-abx/2,-bw/2,0])cube([abx,bw,2]);

  mirror([0,1,0]){
    translate([-adx1/2,aoy,aoz])rotate([arot,0,0])cube([adx1,ady,adx1]);
  }
  translate([-adx1/2,aoy,aoz])rotate([arot,0,0])cube([adx1,ady,adx1]);
}

  mirror([0,1,0]){
    translate([-adx0/2,aoy,aoz+adx1/2-adx0/2])rotate([arot,0,0])cube([adx0,100,adx0]);
  }
  translate([-adx0/2,aoy,aoz+adx1/2-adx0/2])rotate([arot,0,0])cube([adx0,100,adx0]);
  
  
  translate([-acx/2,-acy/2,-0.01])cube([acx,acy,acz]);
  rails();
}


