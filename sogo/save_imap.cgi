#!/usr/bin/perl
#
# sogo-module by Francis Lachapelle <flachapelle@inverse.ca>,
# for webmin by Jamie Cameron

require 'sogo-lib.pl';

&ReadParse();
error_setup($text{'save_err'});

&error($text{'SOGoIMAPServer'})                         unless &defaults_write("SOGoIMAPServer", $in{'SOGoIMAPServer'});
&error($text{'SOGoSieveScriptsEnabled'})                unless &defaults_write("SOGoSieveScriptsEnabled", $in{'SOGoSieveScriptsEnabled'}?"YES":"NO");
&error($text{'SOGoForwardEnabled'})                     unless &defaults_write("SOGoForwardEnabled", $in{'SOGoForwardEnabled'}?"YES":"NO");
&error($text{'SOGoVacationEnabled'})                    unless &defaults_write("SOGoVacationEnabled", $in{'SOGoVacationEnabled'}?"YES":"NO");
&error($text{'SOGoMailAuxiliaryUserAccountsEnabled'})   unless &defaults_write("SOGoMailAuxiliaryUserAccountsEnabled", $in{'SOGoMailAuxiliaryUserAccountsEnabled'}?"YES":"NO");

&webmin_log("save", "imap", "");

&redirect("index.cgi");

