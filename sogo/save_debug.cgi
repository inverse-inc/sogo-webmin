#!/usr/bin/perl
#
# sogo-module by Francis Lachapelle <flachapelle@inverse.ca>,
# for webmin by Jamie Cameron

require 'sogo-lib.pl';

&ReadParse();
error_setup($text{'save_err'});

&error($text{'SOGoUIxDebugEnabled'})                    unless &defaults_write("SOGoUIxDebugEnabled", $in{'SOGoUIxDebugEnabled'}?"YES":"NO");
&error($text{'PGDebugEnabled'})                         unless &defaults_write("PGDebugEnabled", $in{'PGDebugEnabled'}?"YES":"NO");
&error($text{'LDAPDebugEnabled'})                       unless &defaults_write("LDAPDebugEnabled", $in{'LDAPDebugEnabled'}?"YES":"NO");

&webmin_log("save", "debug", "");

&redirect("index.cgi");

