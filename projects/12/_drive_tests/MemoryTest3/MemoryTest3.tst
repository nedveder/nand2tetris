// This file is part of the materials accompanying the book
// "The Elements of Computing Systems" by Nisan and Schocken, 
// MIT Press 2004. Book site: http://www.idc.ac.il/tecs
// File name: projects/12/MemoryTest/MemoryTest.tst.   Version: beta 1.4

load,
output-file MemoryTest3.out,
compare-to MemoryTest3.cmp,
output-list RAM[8000]%D2.6.1 RAM[8001]%D2.6.1 RAM[8002]%D2.6.1 RAM[8003]%D2.6.1 RAM[8004]%D2.6.1 RAM[8005]%D2.6.1;

repeat 10000000 {
  vmstep;
}

output;
