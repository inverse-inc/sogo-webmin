#!/usr/bin/perl
#
# sogo-module by Francis Lachapelle <flachapelle@inverse.ca>,
# for webmin by Jamie Cameron

require 'sogo-lib.pl';

&ReadParse();

popup_header($text{"Tester"});
print ui_subheading($text{"IMAP Access"});

error_setup($text{'module_err'});
eval "use IO::Socket::INET";
popup_error("Please install the IO::Socket::INET Perl module.") if ($@);
popup_error($text{'parameter_err'}) unless ($in{server});

local $sock = IO::Socket::INET->new(PeerAddr => $in{server}, PeerPort => 'smtp(25)');
if ($sock) {
  print "<h3>$text{success}</h3>";
}
else {
  popup_error($text{'failed'} . ': ' . $@);
}

popup_footer();
