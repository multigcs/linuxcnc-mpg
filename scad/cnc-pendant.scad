
$fn=63;


module encoder() {
    color([0.5, 0.5, 0.5, 0.5]) {
        cylinder(d=60, h=7);
        translate([0, 0, 7]) {
            cylinder(d1=60, d2=47, h=4);
        }
        cylinder(d=47, h=24);
        translate([16, 0, 0]) {
            cylinder(d=9, h=36);
        }
    }
}

module encoder_diff(off) {
    translate([0, 0, -10]) {
        cylinder(d=43, h=10.1);
    }

    translate([0, 0, -42]) {
        cylinder(d=61, h=40);
    }

    rotate([0, 0, 60+off]) {
        translate([0, 50.8/2, -10]) {
            cylinder(d=4, h=11);
        }
    }
    rotate([0, 0, 180+off]) {
        translate([0, 50.8/2, -10]) {
            cylinder(d=4, h=11);
        }
    }
    rotate([0, 0, -60+off]) {
        translate([0, 50.8/2, -10]) {
            cylinder(d=4, h=11);
        }
    }

}



module button() {
    translate([0, 0, -3.3/2]) {
        cube([12, 12, 3.3], center=true);
    }
    translate([0, 0, 3.5/2]) {
        cylinder(d=7, h=3.5, center=true);
    }

    translate([5.08/2, 12/2, -4.5]) {
        cylinder(d=1, h=4, center=true);
    }
    translate([5.08/2, -12/2, -4.5]) {
        cylinder(d=1, h=4, center=true);
    }
    translate([-5.08/2, 12/2, -4.5]) {
        cylinder(d=1, h=4, center=true);
    }
    translate([-5.08/2, -12/2, -4.5]) {
        cylinder(d=1, h=4, center=true);
    }
}

module button_diff() {
    translate([0, 0, -3.3/2]) {
        cube([12.5, 12.5, 3.3], center=true);
    }
    translate([0, 0, -9/2]) {
        cube([12.5, 12.5, 9.1], center=true);
    }

    translate([0, 0, 1/2]) {
        cube([10, 10, 1], center=true);
    }
    translate([0, 0, 5/2]) {
        cylinder(d=8, h=5, center=true);
    }

    translate([5.08/2, 12/2, -4.5]) {
        cylinder(d=2, h=6, center=true);
    }
    translate([5.08/2, -12/2, -4.5]) {
        cylinder(d=2, h=6, center=true);
    }
    translate([-5.08/2, 12/2, -4.5]) {
        cylinder(d=2, h=6, center=true);
    }
    translate([-5.08/2, -12/2, -4.5]) {
        cylinder(d=2, h=6, center=true);
    }
}


module rencoder() {
    translate([0, 0, -6.5/2]) {
        cube([12, 12, 6.5], center=true);
    }
    translate([0, 0, 6.5/2]) {
        cylinder(d=7, h=6.5, center=true);
    }
    translate([0, 0, 21/2]) {
        cylinder(d=6, h=21, center=true);
    }

    translate([5.08/2, 15/2, -7]) {
        cylinder(d=1, h=4, center=true);
    }
    translate([0, 15/2, -7]) {
        cylinder(d=1, h=4, center=true);
    }
    translate([5.08/2, -15/2, -7]) {
        cylinder(d=1, h=4, center=true);
    }
    translate([-5.08/2, 15/2, -7]) {
        cylinder(d=1, h=4, center=true);
    }
    translate([-5.08/2, -15/2, -7]) {
        cylinder(d=1, h=4, center=true);
    }
}

module rencoder_diff() {
    translate([0, 0, -6.5/2]) {
        cube([12.5, 12.5, 6.5], center=true);
    }
    translate([0, 0, -9/2]) {
        cube([12.5, 12.5, 9.1], center=true);
    }

    translate([0, 12/2, 0]) {
        cylinder(d=2, h=4, center=true);
    }

    translate([0, 0, 10/2]) {
        cylinder(d=7.5, h=10, center=true);
    }

    translate([5.08/2, 13/2, -4.5]) {
        cube([2, 4, 6], center=true);
    }
    translate([0, 13/2, -4.5]) {
        cube([2, 4, 6], center=true);
    }
    translate([5.08/2, -13/2, -4.5]) {
        cube([2, 4, 6], center=true);
    }
    translate([-5.08/2, 13/2, -4.5]) {
        cube([2, 4, 6], center=true);
    }
    translate([-5.08/2, -13/2, -4.5]) {
        cube([2, 4, 6], center=true);
    }
}

module led3mm(size) {
    cylinder(d=3, h=5.4, center=true);
    translate([0, 0, -2.21]) {
        cylinder(d=3.5, h=1, center=true);
    }
    translate([0, 2.54/2, -5.5]) {
        cylinder(d=1, h=7, center=true);
    }
    translate([0, -2.54/2, -5.5]) {
        cylinder(d=1, h=7, center=true);
    }
}

module led3mm_diff() {
    cylinder(d=3.3, h=10, center=true);

    translate([0, 0, -2.21]) {
        cylinder(d=3.5, h=1, center=true);
    }

    translate([0, 0, -6.75]) {
        cylinder(d=4, h=10, center=true);
    }

}


bd1 = 14.5;
bd1o = bd1/2;
bd1b = -3;
bd1e = 2;
bd1d = -2;

bd2 = 22;
bd2o = -bd2/2;
bd2b = -2;
bd2e = 3;
bd2d = -2;


ch = 15;



module case() {
    difference() {
        union() {
            hull() {
                translate([0, -120, -ch/2]) {
                    cube([90, 65, ch], center=true);
                }
                translate([0, 0, -ch]) {
                    cylinder(d=90, h=ch);
                }
            }
            translate([5, 0, 0]) {
                hull() {
                    translate([0, -120, -ch/2]) {
                        cube([95, 65, ch], center=true);
                    }
                    translate([-60, -120, -ch/2]) {
                        cylinder(d=40, h=ch, center=true);
                    }
                }
            }
        }
        encoder_diff(0);


        hull() {
            translate([0, -120, -ch/2-2]) {
                cube([90-4, 65-4, ch], center=true);
            }
            translate([0, 0, -ch-2]) {
                cylinder(d=90-4, h=ch);
            }
        }
        translate([5, 0, 0]) {
            hull() {
                translate([0, -120, -ch/2-2]) {
                    cube([95-4, 65-4, ch], center=true);
                }
                translate([-60, -120, -ch/2-2]) {
                    cylinder(d=40-4, h=ch, center=true);
                }
            }
            translate([-60, -120, 0]) {
                cylinder(d=22.5, h=70, center=true);
            }
            //lcd hole
            translate([-5, -120, -12+5]) {
                cube([52, 40, 24], center=true);
            }



        }




        for ( i = [-1 : 1] ){
            translate([i * 33, -85, -3]) {
                rencoder_diff();
            }
        }


        translate([-3 * bd1 + bd1o, -45, bd1d]) {
            button_diff();
        }
        translate([2 * bd1 + bd1o, -45, bd1d]) {
            button_diff();
        }


        for ( i = [bd1b : bd1e] ){
            translate([i * bd1 + bd1o, -60, bd1d]) {
                button_diff();
            }
        }

        for ( i = [bd2b : bd2e] ){
            rotate([0, 0, i * bd2 + bd2o]) {
                translate([0, -40, bd2d]) {
                    button_diff();
                }
            }
            rotate([0, 0, i * bd2 + bd2o]) {
                translate([0, -49.2, bd2d]) {
                    led3mm_diff();
                }
            }
        }

        translate([0, -10.2, 0]) {
            for ( i = [bd2b : bd2e] ){
                rotate([0, 0, i * bd2 + bd2o]) {
                    translate([0, -40, bd2d]) {
    //                    led3mm_diff();
                    }
                }
            }
        }

    }



    difference() {
        for ( i = [-1 : 1] ){
            translate([i * 33, -85, -5]) {
                cube([15, 18, 10], center=true);
            }
        }
        for ( i = [-1 : 1] ){
            translate([i * 33, -85, -3]) {
                rencoder_diff();
            }
        }
    }


    difference() {
        translate([-3 * bd1 + bd1o, -45, bd1d-1]) {
                cube([15, 15, 6], center=true);
        }
        translate([-3 * bd1 + bd1o, -45, bd1d]) {
            button_diff();
        }
    }

    difference() {
        translate([2 * bd1 + bd1o, -45, bd1d-1]) {
                cube([15, 15, 6], center=true);
        }
        translate([2 * bd1 + bd1o, -45, bd1d]) {
            button_diff();
        }
    }

    difference() {
        for ( i = [bd1b : bd1e] ){
            translate([i * bd1 + bd1o, -60, bd1d-1]) {
                cube([15, 15, 6], center=true);
            }
        }

        for ( i = [bd1b : bd1e] ){
            translate([i * bd1 + bd1o, -60, bd1d]) {
                button_diff();
            }
        }

    }



    difference() {
        union() {
            for ( i = [bd2b : bd2e] ){
                rotate([0, 0, i * bd2 + bd2o]) {
                    translate([0, -40, bd1d-1]) {
                        cube([15, 15, 6], center=true);
                    }
                }
                rotate([0, 0, i * bd2 + bd2o]) {
                    translate([0, -49.2, bd2d-1]) {
                        cylinder(d=6, h=6, center=true);
                    }
                }
            }

            translate([0, -10.2, 0]) {
                for ( i = [bd2b : bd2e] ){
                    rotate([0, 0, i * bd2 + bd2o]) {
                        translate([0, -40, bd2d-1]) {
    //                      cylinder(d=6, h=6, center=true);
                        }
                    }
                }
            }
        }


        for ( i = [bd2b : bd2e] ){
            rotate([0, 0, i * bd2 + bd2o]) {
                translate([0, -40, bd2d]) {
                    button_diff();
                }
            }
            rotate([0, 0, i * bd2 + bd2o]) {
                translate([0, -49.2, bd2d]) {
                    led3mm_diff();
                }
            }
        }

        translate([0, -10.2, 0]) {
            for ( i = [bd2b : bd2e] ){
                rotate([0, 0, i * bd2 + bd2o]) {
                    translate([0, -40, bd2d]) {
    //                    led3mm_diff();
                    }
                }
            }
        }


    }



    /*
    color([1, 1, 1, 0.6]) {
        for ( i = [-1 : 1] ){
            translate([i * 33, -85, -3]) {
                rencoder();
            }
        }

        for ( i = [bd1b : bd1e] ){
            translate([i * bd1 + bd1o, -60, bd1d]) {
                button();
            }
        }

        translate([-3 * bd1 + bd1o, -45, bd1d]) {
            button();
        }
        translate([2 * bd1 + bd1o, -45, bd1d]) {
            button();
        }



        for ( i = [bd2b : bd2e] ){
            rotate([0, 0, i * bd2 + bd2o]) {
                translate([0, -40, bd1d]) {
                    button();
                }
            }
            rotate([0, 0, i * bd2 + bd2o]) {
                translate([0, -49.2, bd2d]) {
                    led3mm(3);
                }
            }
        }
        translate([0, -10.2, 0]) {
            for ( i = [bd2b : bd2e] ){
                rotate([0, 0, i * bd2 + bd2o]) {
                    translate([0, -40, bd2d]) {
    //                    led3mm(3);
                    }
                }
            }
        }


    }


        translate([0, 0, 0]) {
            encoder();
        }


    */
}




case();







