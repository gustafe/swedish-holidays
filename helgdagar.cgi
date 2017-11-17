#!/usr/bin/perl -wT
# -*- CPerl -*-

use strict;
use lib ("/home/gustaf/prj/Helgdagar/");
use CGI qw(:standard start_ul *table);
use CGI::Carp qw(fatalsToBrowser);
use SwedishHolidays qw( swedish_holidays swedish_weekdays swedish_months );

my $this_year = ( localtime(time) )[5] + 1900;
my ( $day, $mon, $wday ) = ( localtime(time) )[ 3, 4, 6 ];
$mon = $mon + 1;
if ( $wday == 0 ) { $wday = 7 }

my $year = param('ar') || $this_year;

if ( $year !~ m!\d{4}! ) {
    $year = $this_year;
}

my $holidays = swedish_holidays($year);

if ( $year == $this_year ) {
    $holidays->{'Idag'} = {
        date => sprintf( "%4d-%02d-%02d", $year, $mon, $day ),
        DoW  => $wday
    };

}
print header();
print start_html(
    -title => "Helgdagar för $year",
    -lang  => 'sv-SE',
    -head  => [
        Link(
            {
                -rel   => 'stylesheet',
                -type  => 'text/css',
                -media => 'all',
                -href  => 'http://gerikson.com/stylesheets/twitterblog.css'
            }
        )
    ]
);
print h1("Helgdagar för $year");
my $table_rows;
push @$table_rows, th( [ 'Helgdag', 'Datum' ] );

foreach my $holiday (
    sort { $holidays->{$a}->{'date'} cmp $holidays->{$b}->{'date'} }
    keys %{$holidays}
  )
{
    my $date = $holidays->{$holiday}->{'date'};
    my ( $yyyy, $mm, $dd ) = split( '-', $date );
    $dd =~ s/0(\d)/$1/;
    my $wd = swedish_weekdays( $holidays->{$holiday}->{'DoW'} ) . 'en';
    my $MM = swedish_months($mm);
    if ( $holiday eq 'Idag' ) { $holiday = b($holiday) }
    push @$table_rows, td( [ $holiday, "$wd den $dd $MM" ] );
}

#print '</table>';
print table( { -valign => 'top' }, Tr( {}, $table_rows ) );
print '<p>Helgdagar i framtiden: ';
for ( my $i = $year + 1 ; $i < $year + 6 ; $i++ ) {
    print a( { -href => "helgdagar.cgi?ar=$i", -title => "Helgdagar för $i" },
        $i );
    print '&nbsp;';
}
print '</p>';
print p(
    a(
        { -href => "helgdagar.cgi", -title => "Årets helgdagar" },
        "Tillbaka till $this_year"
    )
);
print hr();
print "<address>",
  a( { -href => "http://gerikson.com/blog/" }, "&copy; 2005 Gustaf Erikson" ),
  "</address>";

print end_html()
