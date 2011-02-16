#!/usr/bin/perl
#
# sogo-module by Francis Lachapelle <flachapelle@inverse.ca>,
# for webmin by Jamie Cameron
#


require 'sogo-lib.pl';

&ui_print_header(undef, $text{'index_title'} . ' / ' . $text{'sources_title'}, "", undef, 1, 1);

if (!-x $config{'gnustep_defaults_command'}) {
  print &text('index_edefaults',
	      "<tt>$config{'gnustep_defaults_command'}</tt>",
	      "../config.cgi?$module_name"),"<p>\n";
  &ui_print_footer("", $text{'index_return'});
  exit;
}

print <<EOS
<script lang="javascript">
function popup_test(alink, param, value) {
  var url = alink.href + '?' + param + '=' + encodeURIComponent(value);
  window.open(url, "_blank",
              "width=300,height=150,resizable=1,scrollbars=0,location=0");

  return false;
}
</script>
EOS
;

@sources = &defaults_read_array("SOGoUserSources");

print &ui_form_start("delete_source.cgi", "post");
@rowlinks = ( &select_all_link("d", 0),
	      &select_invert_link("d", 0),
	      "<a href='add_source.cgi'>$text{'add_source'}</a>");
#print &ui_links_row(\@rowlinks);
print &ui_columns_start([ "", $text{'SOGoUserSource_id'},
			  $text{'SOGoUserSource_type'},
			  $text{'SOGoUserSource_canAuthenticate?'},
			  $text{'SOGoUserSource_isAddressBook?'},
			  $text{'test'} ], 100);
foreach $source (@sources) {
  local @cols;
  my $s = &string2hash($source);
  push(@cols, "<a href='edit_source.cgi?id=$s->{id}'>".
       &html_escape($s->{id})."</a>");
  push(@cols, $s->{type});
  push(@cols, $s->{canAuthenticate} =~ /yes/i ? $text{'yes'} : $text{'no'});
  push(@cols, $s->{isAddressBook} =~ /yes/i ? $text{'yes'} : $text{'no'});
  push(@cols, "<a href='test_ldap.cgi' onClick=\"return popup_test(this, 'id', '$s->{id}');\">$text{'test'}</a>") if ($s->{type} eq 'ldap');
  push(@cols, "<a href='test_database.cgi' onClick=\"return popup_test(this, 'url', '$s->{viewURL}');\">$text{'test'}</a>") if ($s->{type} eq 'sql');
  print &ui_checked_columns_row(\@cols, undef, "d", $s->{id});
}
print &ui_columns_end();
print &ui_links_row(\@rowlinks);
print &ui_form_end([ [ "delete", $text{'SOGoUserSource_delete'} ] ]);

&ui_print_footer("", $text{'index_return'});
