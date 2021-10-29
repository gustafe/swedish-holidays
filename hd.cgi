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

my $holidays = swedish_holidays($year);
my %data = ( holidays => [sort {$a->{date} cmp $b->{date}} @$holidays] );
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
__END__
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
