#!/usr/bin/perl
#
# sogo-module by Francis Lachapelle <flachapelle@inverse.ca>,
# for webmin by Jamie Cameron

require 'sogo-lib.pl';

&ReadParse();

popup_header($text{"Tester"});
print ui_subheading($text{"SMTP Access"});

error_setup($text{'module_err'});
eval "use Net::SMTP";
popup_error("Please install the Net::SMTP Perl module.") if ($@);
popup_error($text{'parameter_err'}) unless ($in{server});

local $smtp = Net::SMTP->new($in{server}, Timeout => 10);
if ($smtp) {
  print "<h3>$text{success}</h3>";
}
else {
  popup_error($text{'failed'} . ': ' . $@);
}

popup_footer();
