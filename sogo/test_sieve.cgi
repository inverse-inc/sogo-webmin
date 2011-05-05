#!/usr/bin/perl
#
# sogo-module by Francis Lachapelle <flachapelle@inverse.ca>,
# for webmin by Jamie Cameron

require 'sogo-lib.pl';

&ReadParse();

popup_header($text{"Tester"});
print ui_subheading($text{"Sieve Access"});

error_setup($text{'module_err'});
eval "use IO::Socket::INET";
popup_error("Please install the IO::Socket::INET Perl module.") if ($@);
popup_error($text{'parameter_err'}) unless ($in{server});

my $server = $in{server};
my $port = '2000';
if ($server =~ m/sieve:\/\/([^:]+)(:(\d+))?/) {
  $server = $1;
  $port = "$3" if (defined $3);
}

local $sock = IO::Socket::INET->new(Proto => "tcp",
                                    PeerAddr => $server,
                                    PeerPort => $port,
                                    Timeout => 10);
if ($sock) {
  print "<h3>$text{success} ($server:$port)</h3>";
}
else {
  popup_error($text{'failed'} . ': ' . $@);
}

popup_footer();
