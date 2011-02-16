#!/usr/bin/perl
#
# sogo-module by Francis Lachapelle <flachapelle@inverse.ca>,
# for webmin by Jamie Cameron

require 'sogo-lib.pl';

&ReadParse();
error_setup($text{'save_err'});

&error($text{'SOGoProfileURL'})                         unless &defaults_write("SOGoProfileURL", $in{'SOGoProfileURL'});
&error($text{'OCSFolderInfoURL'})                       unless &defaults_write("OCSFolderInfoURL", $in{'OCSFolderInfoURL'});
&error($text{'OCSEMailAlarmsFolderURL'})                unless &defaults_write("OCSEMailAlarmsFolderURL", $in{'OCSEMailAlarmsFolderURL'});
&error($text{'OCSSessionsFolderURL'})                   unless &defaults_write("OCSSessionsFolderURL", $in{'OCSSessionsFolderURL'});
&webmin_log("save", "database", "");

&redirect("index.cgi");
