#!/usr/bin/perl
#
# sogo-module by Francis Lachapelle <flachapelle@inverse.ca>,
# for webmin by Jamie Cameron
#


require 'sogo-lib.pl';

&ui_print_header(undef, $text{'index_title'} . ' / ' . $text{'smtp_title'}, "", undef, 1, 1);

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

print &ui_form_start("save_smtp.cgi", "post", undef, "name=smtp");

# SMTP
print &ui_table_start($text{'smtp_title'}, "width=100%", 2, "smtp");
print &ui_table_row($text{'SOGoMailingMechanism'},
 		    &ui_radio("SOGoMailingMechanism",
			      &defaults_read("SOGoMailingMechanism") || "sendmail",
			      [ [ "sendmail", "sendmail binary" ],
				[ "smtp", "SMTP server" ] ]) . 
		   &ui_textbox("SOGoSMTPServer",
			       &defaults_read("SOGoSMTPServer"),
			       30) .
		   "&nbsp;<a href='test_smtp.cgi' onClick='return popup_test(this, document.smtp.SOGoSMTPServer);'>$text{'test'}</a>");
print &ui_hidden_table_end("smtp");

print &ui_form_end([ [ undef, $text{'save'}, $text{'note_restart'} ] ]);

&ui_print_footer("", $text{'index_return'});
