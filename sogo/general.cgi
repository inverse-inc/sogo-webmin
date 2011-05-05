#!/usr/bin/perl
#
# sogo-module by Francis Lachapelle <flachapelle@inverse.ca>,
# for webmin by Jamie Cameron
#

require 'sogo-lib.pl';

&ui_print_header(undef, $text{'index_title'} . ' / ' . $text{'general_title'}, "", undef, 1, 1);

if (!-x $config{'gnustep_defaults_command'}) {
  print &text('index_edefaults',
	      "<tt>$config{'gnustep_defaults_command'}</tt>",
	      "../config.cgi?$module_name"),"<p>\n";
  &ui_print_footer("", $text{'index_return'});
  exit;
}

print &ui_form_start("save_general.cgi", "post");

# General
print &ui_table_start($text{'general_title'}, "width=100%", 2, "general");
print &ui_table_row($text{'WOWorkersCount'},
		    &ui_textbox("WOWorkersCount",
				&defaults_read("WOWorkersCount") || 3,
				3));
print &ui_table_row($text{'WOLogFile'},
		    &ui_textbox("WOLogFile",
				&defaults_read("WOLogFile") || "/var/log/sogo/sogo.log",
				40));
print &ui_table_row($text{'SOGoLanguage'},
		    &ui_select("SOGoLanguage",
			       &defaults_read("SOGoLanguage") || "English",
                               # Extracted from SoObjects/SOGo/SOGoDefaults.plist
                               [ "Catalan", "Czech", "Welsh", "English", "Spanish",
                               "French", "German", "Italian", "Hungarian",
                               "Dutch", "BrazilianPortuguese", "Norwegian", "Polish",
                               "Russian", "Ukrainian", "Swedish" ],
			       1,
			       0,
			       1 # add if missing
			       ));
print &ui_table_row($text{'SOGoTimeZone'},
		    &ui_select("SOGoTimeZone",
			       &defaults_read("SOGoTimeZone") || "UTC",
			       &get_timezones,
			       1,
			       0,
			       1 # add if missing
			       ));
print &ui_table_row($text{'SOGoMailDomain'},
		    &ui_textbox("SOGoMailDomain",
				&defaults_read("SOGoMailDomain") || &get_system_hostname(),
				30));
print &ui_table_row($text{'SOGoAppointmentSendEMailNotifications'},
		    &ui_checkbox("SOGoAppointmentSendEMailNotifications",
				 "YES",
				 undef,
				 &defaults_read_bool("SOGoAppointmentSendEMailNotifications")));
print &ui_table_row($text{'SOGoFoldersSendEMailNotifications'},
		    &ui_checkbox("SOGoFoldersSendEMailNotifications",
				 "YES",
				 undef,
				 &defaults_read_bool("SOGoFoldersSendEMailNotifications")));
print &ui_table_row($text{'SOGoACLsSendEMailNotifications'},
		    &ui_checkbox("SOGoACLsSendEMailNotifications",
				 "YES",
				 undef,
				 &defaults_read_bool("SOGoACLsSendEMailNotifications")));
print &ui_table_row($text{'SOGoEnableEMailAlarms'},
		    &ui_checkbox("SOGoEnableEMailAlarms",
				 "YES",
				 undef,
				 &defaults_read_bool("SOGoEnableEMailAlarms")));
print &ui_table_row($text{'SOGoSuperUsernames'},
		    &ui_textarea("SOGoSuperUsernames",
				 join("\n", &defaults_read_array("SOGoSuperUsernames")),
				 5,
				 40,
				 "off"));
print &ui_hidden_table_end("general");

print &ui_form_end([ [ undef, $text{'save'}, $text{'note_restart'} ] ]);

&ui_print_footer("", $text{'index_return'});
