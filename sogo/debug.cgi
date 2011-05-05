#!/usr/bin/perl
#
# sogo-module by Francis Lachapelle <flachapelle@inverse.ca>,
# for webmin by Jamie Cameron
#


require 'sogo-lib.pl';

&ui_print_header(undef, $text{'index_title'} . ' / ' . $text{'debug_title'}, "", undef, 1, 1);

if (!-x $config{'gnustep_defaults_command'}) {
  print &text('index_edefaults',
	      "<tt>$config{'gnustep_defaults_command'}</tt>",
	      "../config.cgi?$module_name"),"<p>\n";
  &ui_print_footer("", $text{'index_return'});
  exit;
}

print &ui_form_start("save_debug.cgi", "post");

# Debugging
print &ui_table_start($text{'debug_title'}, "width=100%", 2, "debug");
print &ui_table_row($text{'SOGoUIxDebugEnabled'},
		    &ui_checkbox("SOGoUIxDebugEnabled",
				 "YES",
				 undef,
				 &defaults_read_bool("SOGoUIxDebugEnabled")));
print &ui_table_row($text{'PGDebugEnabled'},
		    &ui_checkbox("PGDebugEnabled",
				 "YES",
				 undef,
				 &defaults_read_bool("PGDebugEnabled")));
print &ui_table_row($text{'LDAPDebugEnabled'},
		    &ui_checkbox("LDAPDebugEnabled",
				 "YES",
				 undef,
				 &defaults_read_bool("LDAPDebugEnabled")));
print &ui_hidden_table_end("debug");

print &ui_form_end([ [ undef, $text{'save'}, $text{'note_restart'} ] ]);

&ui_print_footer("", $text{'index_return'});
