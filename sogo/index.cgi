#!/usr/bin/perl
#
# sogo-module by Francis Lachapelle <flachapelle@inverse.ca>,
# for webmin by Jamie Cameron

require 'sogo-lib.pl';

&ui_print_header(undef, $text{'index_title'}, "", undef, 1, 1);

if (!-x $config{'gnustep_defaults_command'}) {
  print &text('index_edefaults',
	      "<tt>$config{'gnustep_defaults_command'}</tt>",
	      "../config.cgi?$module_name"),"<p>\n";
  &ui_print_footer("/", $text{'index'});
  exit;
}

@onames =  ( "general", "sources", "database", "smtp", "imap", "debug" );
foreach $oitem (@onames) {
  push (@olinks, $oitem . ".cgi");
  push (@otitles, $text{$oitem . "_title"});
  push (@oicons, "images/" . $oitem . ".gif");
}
&icons_table(\@olinks, \@otitles, \@oicons);

if (&status_daemon() == 0) {
  print &ui_form_start("stop.cgi", "post");
  print &ui_form_end([ [ undef, $text{'stop'} ] ]);
  print &ui_form_start("restart.cgi", "post");
  print &ui_form_end([ [ undef, $text{'restart'}, $text{'note_apply'} ] ]);
}
elsif (&status_daemon() > 1) { 
  print &ui_form_start("start.cgi", "post");
  print &ui_form_end([ [ undef, $text{'start'} ] ]);
}

&ui_print_footer("/", $text{'index'});
