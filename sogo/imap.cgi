#!/usr/bin/perl
#
# sogo-module by Francis Lachapelle <flachapelle@inverse.ca>,
# for webmin by Jamie Cameron
#


require 'sogo-lib.pl';

&ui_print_header(undef, $text{'index_title'} . ' / ' . $text{'imap_title'}, "", undef, 1, 1);

if (!-x $config{'gnustep_defaults_command'}) {
  print &text('index_edefaults',
	      "<tt>$config{'gnustep_defaults_command'}</tt>",
	      "../config.cgi?$module_name"),"<p>\n";
  &ui_print_footer("", $text{'index_return'});
  exit;
}

print <<EOS
<style type="text/css">
TD SPAN {
 font-size: smaller;
}
</style>
EOS
;

print <<EOS
<script lang="javascript">
function popup_test(alink, object) {
  if (object.value) {
    var url = alink.href + '?server=' + encodeURIComponent(object.value);
    window.open(url, "_blank",
                "width=300,height=150,resizable=1,scrollbars=0,location=0");
  }
  return false;
}
</script>
EOS
;

print &ui_form_start("save_imap.cgi", "post", undef, "name=imap");

# IMAP
print &ui_table_start($text{'imap_title'}, "width=100%", 2, "imap");
print &ui_table_row($text{'SOGoIMAPServer'},
		    &ui_textbox("SOGoIMAPServer",
				&defaults_read("SOGoIMAPServer") || 'localhost',
				30) .
		   "&nbsp;<a href='test_imap.cgi' onClick='return popup_test(this, document.imap.SOGoIMAPServer);'>$text{'test'}</a>" .
                   '<br/><span>' . $text{SOGoIMAPServer_note} . '</span>');
print &ui_table_row($text{'SOGoSieveServer'},
		    &ui_textbox("SOGoSieveServer",
				&defaults_read("SOGoSieveServer") || 'sieve://localhost',
				30) .
		   "&nbsp;<a href='test_sieve.cgi' onClick='return popup_test(this, document.imap.SOGoSieveServer);'>$text{'test'}</a>" .
                   '<br/><span>' . $text{SOGoSieveServer_note} . '</span>');
print &ui_table_row($text{'SOGoSieveScriptsEnabled'},
		    &ui_checkbox("SOGoSieveScriptsEnabled",
				 "YES",
				 undef,
				 &defaults_read_bool("SOGoSieveScriptsEnabled")));
print &ui_table_row($text{'SOGoForwardEnabled'},
		    &ui_checkbox("SOGoForwardEnabled",
				 "YES",
				 undef,
				 &defaults_read_bool("SOGoForwardEnabled")));
print &ui_table_row($text{'SOGoVacationEnabled'},
		    &ui_checkbox("SOGoVacationEnabled",
				 "YES",
				 undef,
				 &defaults_read_bool("SOGoVacationEnabled")));
print &ui_table_row($text{'SOGoMailAuxiliaryUserAccountsEnabled'},
		    &ui_checkbox("SOGoMailAuxiliaryUserAccountsEnabled",
				 "YES",
				 undef,
				 &defaults_read_bool("SOGoMailAuxiliaryUserAccountsEnabled")));
print &ui_hidden_table_end("imap");

print &ui_form_end([ [ undef, $text{'save'}, $text{'note_restart'} ] ]);

&ui_print_footer("", $text{'index_return'});
