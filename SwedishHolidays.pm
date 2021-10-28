package SwedishHolidays; # -*- CPerl -*-

@ISA = ('Exporter');
@EXPORT = qw( &swedish_holidays &swedish_weekdays &swedish_months );

use Date::Calc qw(Day_of_Week Add_Delta_YMD Easter_Sunday Today_and_Now);

sub date_info {
    my @date = @_;
    my $date_format = "%d-%02d-%02d";
    my $day_of_week = Day_of_Week( @date );
    my $dt_string = sprintf($date_format, @date);
    my $date = { 'date' => $dt_string, 'DoW' => $day_of_week };
    return $date;
}


sub add_day {
    my $delta = pop @_;
    my @date = @_;
    return Add_Delta_YMD( @date, 0,0,$delta );
}


sub swedish_holidays {

    # Given a year as an argument, return as hash reference with the
    # names of the holidays in Swedish as keys. The values are a hash
    # reference with the ISO date ('date') and the day of week ('DoW')
    # as values.

    my $year = shift;
    die "year out of range (1583 to 2299) or bad format: $year\n" if (( $year < 1583 or $year > 2299) or $year !~ m/\d{4}/) ;

    ### constants

    my $MS_MIN = '06-20'; # midsummer's day is first Saturday after this date
    my $AH_MIN = '10-31'; # All Saints Day is first Saturday after this date

    my $fixed_dates = { 'Nyårsdagen' => '01-01',           # New Years Day
			'Trettondagen' =>	'01-06',   # Epiphany
			'Första maj' => '05-01',           # May Day
			'Sveriges nationaldag' => '06-06', # National day
			'Juldagen' => '12-25',             # Christmas Day 
			'Annandag jul' =>	'12-26'};  # Boxing day

    my $holidays = {};
    ### calculate moveable feasts 

    my @paskdagen = Easter_Sunday( $year );
    $holidays->{'Påskdagen'} = date_info( @paskdagen );                              # Easter Day
    $holidays->{'Långfredagen'} = date_info( add_day( @paskdagen, -2 ));             # Good Friday
    $holidays->{'Annandag påsk'} = date_info( add_day( @paskdagen, 1 ));             # Day after Easter Day
    $holidays->{'Kristi Himmelsfärdsdagen'} = date_info( add_day( @paskdagen, 39 )); # Ascension Day
    $holidays->{'Pingstdagen'} = date_info( add_day( @paskdagen, 49 ));              # Pentecost

    # search for first Saturday after some dates
    my @midsommar = ( $year, split('-', $MS_MIN) );
    while ( Day_of_Week(@midsommar) != 6 ) {
	@midsommar = add_day( @midsommar, 1 );
    }
    $holidays->{'Midsommardagen'} = date_info( @midsommar ); # Midsummer's day

    my @allhelgona = ( $year, split('-', $AH_MIN) );
    while ( Day_of_Week(@allhelgona) != 6 ) {
	@allhelgona = add_day( @allhelgona,1 );
    }
    $holidays->{'Alla helgons dag'} = date_info( @allhelgona ); # All Saints

    foreach my $holiday ( keys %{$fixed_dates} ) {
	my $date = $fixed_dates->{$holiday};
	$holidays->{$holiday} = date_info($year, split('-', $date));
    }
    return $holidays;
}

sub swedish_weekdays {
    my @wd_names = qw(måndag tisdag onsdag torsdag fredag lördag söndag);
    my $DoW = shift;
    die "weekday index out of range (1 to 7) or bad format: $DoW\n" unless (( $DoW > 0 and $DoW < 8 ) and $DoW =~ m/\d{1}/ );
#    return $DoW;
    return $wd_names[$DoW - 1];

}

sub swedish_months {
    my @month_names = qw ( januari februari mars april maj juni juli augusti september oktober november december );
    my $mon = shift;
    die "month index out of range (1 to 12) or bad format: $mon\n" unless (( $mon > 0 and $mon < 13) and $mon =~ m/\d+/ );
    return $month_names[$mon - 1];
}

1;
