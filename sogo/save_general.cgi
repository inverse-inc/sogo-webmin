#!/usr/bin/perl
#
# sogo-module by Francis Lachapelle <flachapelle@inverse.ca>,
# for webmin by Jamie Cameron

require 'sogo-lib.pl';

&ReadParse();
error_setup($text{'save_err'});

&error($text{'WOWorkersCount'})                         unless &defaults_write("WOWorkersCount", int($in{'WOWorkersCount'}));
&error($text{'WOLogFile'})                              unless &defaults_write("WOLogFile", $in{'WOLogFile'});
&error($text{'SOGoLanguage'})                           unless &defaults_write("SOGoLanguage", $in{'SOGoLanguage'});
&error($text{'SOGoTimeZone'})                           unless &defaults_write("SOGoTimeZone", $in{'SOGoTimeZone'});
&error($text{'SOGoAppointmentSendEMailNotifications'})  unless &defaults_write("SOGoAppointmentSendEMailNotifications", $in{'SOGoAppointmentSendEMailNotifications'}?"YES":"NO");
&error($text{'SOGoFoldersSendEMailNotifications'})      unless &defaults_write("SOGoFoldersSendEMailNotifications", $in{'SOGoFoldersSendEMailNotifications'}?"YES":"NO");
&error($text{'SOGoACLsSendEMailNotifications'})         unless &defaults_write("SOGoACLsSendEMailNotifications", $in{'SOGoACLsSendEMailNotifications'}?"YES":"NO");
&error($text{'SOGoEnableEMailAlarms'})                  unless &defaults_write("SOGoEnableEMailAlarms", $in{'SOGoEnableEMailAlarms'}?"YES":"NO");
@superusernames = split("\n", $in{'SOGoSuperUsernames'});
&error($text{'SOGoSuperUsernames'})                     unless &defaults_write_array("SOGoSuperUsernames", \@superusernames);

&webmin_log("save", "general", "");

&redirect("index.cgi");

