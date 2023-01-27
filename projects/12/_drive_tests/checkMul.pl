#!/usr/bin/perl -w
use strict;
my $fileName = shift;

open(my $IN, "<", $fileName) or die "Can not open file $fileName\n";

while (my $line = <$IN>){
  print $line;
}
