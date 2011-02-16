#!/usr/bin/perl
#
# sogo-module by Francis Lachapelle <flachapelle@inverse.ca>,
# for webmin by Jamie Cameron
#


require 'sogo-lib.pl';

&ui_print_header(undef, $text{'index_title'} . ' / ' . $text{'database_title'}, "", undef, 1, 1);

if (!-x $config{'gnustep_defaults_command'}) {
  print &text('index_edefaults',
	      "<tt>$config{'gnustep_defaults_command'}</tt>",
	      "../config.cgi?$module_name"),"<p>\n";
  &ui_print_footer("", $text{'index_return'});
  exit;
}

print <<EOS
<script lang="javascript">
function popup_test(alink, object) {
  var url = alink.href + '?url=' + encodeURIComponent(object.value);
  window.open(url, "_blank",
              "width=300,height=150,resizable=1,scrollbars=0,location=0");

  return false;
}
</script>
EOS
;

print &ui_form_start("save_database.cgi", "post", undef, "name=database");

# Database
print &ui_table_start($text{'database_title'}, "width=100%", 2, "database");
print &ui_table_row('', $text{database_format});
print &ui_table_row($text{'SOGoProfileURL'},
		    &ui_textbox("SOGoProfileURL",
				&defaults_read("SOGoProfileURL"),
				80) .
		    "&nbsp;<a href='test_database.cgi' onClick='return popup_test(this, document.database.SOGoProfileURL);'>$text{'test'}</a>");
print &ui_table_row($text{'OCSFolderInfoURL'},
		    &ui_textbox("OCSFolderInfoURL",
				&defaults_read("OCSFolderInfoURL"),
				80) .
		    "&nbsp;<a href='test_database.cgi' onClick='return popup_test(this, document.database.OCSFolderInfoURL);'>$text{'test'}</a>");
print &ui_table_row($text{'OCSEMailAlarmsFolderURL'},
		    &ui_textbox("OCSEMailAlarmsFolderURL",
				&defaults_read("OCSEMailAlarmsFolderURL"),
				80) .
		    "&nbsp;<a href='test_database.cgi' onClick='return popup_test(this, document.database.OCSEMailAlarmsFolderURL);'>$text{'test'}</a>");
print &ui_table_row($text{'OCSSessionsFolderURL'},
		    &ui_textbox("OCSSessionsFolderURL",
				&defaults_read("OCSSessionsFolderURL"),
				80) .
		    "&nbsp;<a href='test_database.cgi' onClick='return popup_test(this, document.database.OCSSessionsFolderURL);'>$text{'test'}</a>");
print &ui_hidden_table_end("database");

print &ui_form_end([ [ undef, $text{'save'}, $text{'note_restart'} ] ]);

&ui_print_footer("", $text{'index_return'});
