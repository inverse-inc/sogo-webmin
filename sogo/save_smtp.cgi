#!/usr/bin/perl
#
# sogo-module by Francis Lachapelle <flachapelle@inverse.ca>,
# for webmin by Jamie Cameron

require 'sogo-lib.pl';

&ReadParse();
error_setup($text{'save_err'});

&error($text{'SOGoMailingMechanism'})                   unless &defaults_write("SOGoMailingMechanism", $in{'SOGoMailingMechanism'});
&error($text{'SOGoSMTPServer'})                         unless &defaults_write("SOGoSMTPServer", $in{'SOGoSMTPServer'});

&webmin_log("save", "smtp", "");

&redirect("index.cgi");

