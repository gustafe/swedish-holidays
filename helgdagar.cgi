#!/usr/bin/perl -w
# -*- CPerl -*-

use strict;
use lib ("/home/gustaf/prj/Helgdagar/", "/home/gustaf/perl5/lib/perl5/");
use CGI qw(:standard start_ul *table);
use CGI::Carp qw(fatalsToBrowser);
use SwedishHolidays qw( swedish_holidays swedish_weekdays swedish_months );

my $this_year = (localtime(time))[5] + 1900;
my $year =  param('ar') || $this_year;

if ( $year !~ m!\d{4}! ) {
    $year = $this_year }

my $holidays = swedish_holidays( $year );
print header();
print start_html( -title => "Helgdagar för $year", -lang=>'sv-SE', -head =>[
				   Link({
					 -rel=>'stylesheet',
					 -type=>'text/css',
					 -media=>'all',
					 -href=>'http://gerikson.com/stylesheets/twitterblog.css'})]);
print h1("Helgdagar för $year");
print '<table>';
print "<tr valign='top'><th>Helgdag</th><th>Datum</th></tr>\n";
foreach my $holiday ( sort{ $holidays->{$a}->{'date'} cmp $holidays->{$b}->{'date'} } keys %{$holidays} ) {
    my $date = $holidays->{$holiday}->{'date'};
    my ( $yyyy, $mm, $dd ) = split('-', $date);
    $dd =~ s/0(\d)/$1/;
    my $wd = swedish_weekdays( $holidays->{$holiday}->{'DoW'} ) . 'en';
    my $MM = swedish_months( $mm );
    print '<tr><td>', $holiday, "</td><td>$wd den $dd $MM</td>", "</tr>\n";
#    print "$date\t$holiday\t$wd den $dd $MM\n";
}
print '</table>';
print '<p>Helgdagar i framtiden: ';
for ( my $i = $year+1; $i < $year + 6; $i++ ) {
    print a({ -href => "helgdagar.cgi?ar=$i", -title => "Helgdagar för $i"}, $i);
    print '&nbsp;';
}
print '</p>';
print p(a({ -href => "helgdagar.cgi", -title => "Årets helgdagar"}, "Tillbaka till $this_year"));
print hr();
print "<address>", a({ -href => "http://gerikson.com/blog/" }, "&copy; 2005 Gustaf Erikson"), "</address>";

print end_html()
