#!/usr/bin/perl -wT
# -*- CPerl -*-
use Modern::Perl qw/2014/;
use strict;
#binmode STDOUT, ":encoding(utf8)";
#use File::Basename;
#use File::Spec;
use FindBin qw/$Bin/;
BEGIN {
    if ($Bin =~ m!([\w\./\-]+)!) {
	$Bin = $1;
    } else {
	die "Bad directory $Bin";
    }
}
use Template;
use lib "$Bin/lib";
use CGI qw(:standard start_ul *table -utf8);

use CGI::Carp qw(fatalsToBrowser);
use SwedishHolidays qw( swedish_holidays );

my $this_year = ( localtime(time) )[5] + 1900;
my ( $day, $mon, $wday ) = ( localtime(time) )[ 3, 4, 6 ];
$mon = $mon + 1;
if ( $wday == 0 ) { $wday = 7 }
my $year = $ENV{QUERY_STRING} || $this_year;
if ( $year !~ m!^\d{4}$! ) {
    $year = $this_year;
}
my %env;
for my $k (keys %ENV) {
    $env{$k} = $ENV{$k};
}
my $holidays = swedish_holidays($year);
my %data = ( holidays => [sort {$a->{date} cmp $b->{date}} @$holidays] );
$data{env} = \%env;
$data{year}=$year;
#for my $el (sort {$a->{date} cmp $b->{date}} @$holidays) {
#    say "$el->{date} $el->{holiday} $el->{sw_date} ", $el->{legal}!=1?'*':'';
#}
my $tt = Template->new( {INCLUDE_PATH=>"$Bin/templates"});
my $out; my $template;
$out= "20 text/gemini; lang=sv\r\n";
$template='hd.tt';

$tt->process( $template, \%data,\$out) or die $tt->error();
print $out;
