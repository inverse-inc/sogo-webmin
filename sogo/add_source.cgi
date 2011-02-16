#!/usr/bin/perl
#
# sogo-module by Francis Lachapelle <flachapelle@inverse.ca>,
# for webmin by Jamie Cameron
#
# add_source.cgi - Display a form for adding a source

require 'sogo-lib.pl';

&ui_print_header(undef, $text{'index_title'} . ' / ' . $text{'sources_title'} . ' / ' . $text{'add_source'}, "");

print <<EOS
<style type="text/css">
TABLE#SQL_options {
  display: none;
}
TABLE#LDAP_options {
 width: 600px;
}
TD.ui_label {
 text-align: right;
}
TD SPAN {
 font-size: smaller;
}
</style>
EOS
;

print <<EOS
<script lang="javascript">
function onChangeType(list) {
  if (list.value == 'sql') {
    hide('LDAP_options');
    show('SQL_options');
  }
  else {
    hide('SQL_options');
    show('LDAP_options');
  }
}
function hide(id) {
  if (document.getElementById) // DOM3 = IE5, NS6
    document.getElementById(id).style.display = 'none';
  else {
    if (document.layers) // Netscape 4
      document.id.display = 'none';
    else // IE 4
      document.all.id.style.display = 'none';
  }
}

function show(id) {
  if (document.getElementById) // DOM3 = IE5, NS6
    document.getElementById(id).style.display = 'block';
  else {
    if (document.layers) // Netscape 4
      document.id.display = 'block';
    else // IE 4
      document.all.id.style.display = 'block';
  }
}
</script>
EOS
;

# Start of the form
print &ui_form_start("save_source.cgi", "post");
print &ui_table_start($text{'source_title'}, undef, 2);
#print &ui_table_row($text{'SOGoUserSources'},
#		    &ui_textarea("SOGoUserSource",
#				 undef,
#				 12,
#				 40,
#				 "off"));
print &ui_table_row($text{'SOGoUserSource_id'},
		    &ui_textbox("SOGoUserSource_id",
				undef,
				40));
print &ui_table_row($text{'SOGoUserSource_displayName'},
		    &ui_textbox("SOGoUserSource_displayName",
				undef,
				40));
print &ui_table_row($text{'SOGoUserSource_canAuthenticate'},
		    &ui_checkbox("SOGoUserSource_canAuthenticate",
				 "YES",
                                 undef,
                                 1));
print &ui_table_row($text{'SOGoUserSource_isAddressBook'},
		    &ui_checkbox("SOGoUserSource_isAddressBook",
				 "YES",
                                 undef,
                                 1));
print &ui_table_row($text{'SOGoUserSource_type'},
		    &ui_select("SOGoUserSource_type",
			       "ldap",
			       [ "ldap", "sql" ],
			       1,
			       0,
			       0,
			       0,
			       'onChange=onChangeType(this)'));
print &ui_table_end();

print &ui_table_start($text{'SOGoUserSource_ldap'}, 'id="LDAP_options"', 2);
print &ui_table_row($text{'ldap_hostname'},
		    &ui_textarea("ldap_hostname",
				 undef,
				 3,
				 40,
				 "off"));
print &ui_table_row($text{'ldap_port'},
		    &ui_textbox("ldap_port",
				"389",
				5));
print &ui_table_row($text{'ldap_encryption'},
		    &ui_select("ldap_encryption",
			       "None",
			       [ "None", "SSL", "STARTTLS" ],
			       1,
			       0,
			       0
			       ));
print &ui_table_row($text{'ldap_CNFieldName'},
		    &ui_textbox("ldap_CNFieldName",
				"cn",
				20));
print &ui_table_row($text{'ldap_IDFieldName'},
		    &ui_textbox("ldap_IDFieldName",
				"uid",
				20));
print &ui_table_row($text{'ldap_UIDFieldName'},
		    &ui_textbox("ldap_UIDFieldName",
				"uid",
				20));
print &ui_table_row($text{'ldap_MailFieldNames'},
		    &ui_textarea("ldap_MailFieldNames",
				 undef,
				 3,
				 40,
				 "off"));
print &ui_table_row($text{'ldap_IMAPHostFieldName'},
		    &ui_textbox("ldap_IMAPHostFieldName",
				undef,
				20));
print &ui_table_row($text{'ldap_baseDN'},
		    &ui_textbox("ldap_baseDN",
				undef,
				40));
print &ui_table_row($text{'ldap_filter'},
		    &ui_textbox("ldap_filter",
				undef,
				40));
print &ui_table_row($text{'ldap_scope'},
		    &ui_select("ldap_scope",
			       "SUB",
			       [ "BASE", "ONE", "SUB" ],
			       1,
			       0,
			       0
			       ));
print &ui_table_row($text{'ldap_bindDN'},
		    &ui_textbox("ldap_bindDN",
				undef,
				40));
print &ui_table_row($text{'ldap_bindPassword'},
		    &ui_password("ldap_bindPassword",
				undef,
				20));
print &ui_table_row($text{'ldap_bindFields'},
		    &ui_textarea("ldap_bindFields",
				 undef,
				 3,
				 40,
				 "off"));
print &ui_table_row($text{'SOGoLDAPContactInfoAttribute'},
		    &ui_textbox("SOGoLDAPContactInfoAttribute",
				undef,
				20));
print &ui_table_row($text{'SOGoLDAPQueryLimit'},
		    &ui_textbox("SOGoLDAPQueryLimit",
				undef,
				8));
print &ui_table_row($text{'SOGoLDAPQueryTimeout'},
		    &ui_textbox("SOGoLDAPQueryTimeout",
				undef,
				8));
print &ui_table_row($text{'ldap_passwordPolicy'},
		    &ui_checkbox("ldap_passwordPolicy",
				 "YES"));
# print &ui_table_row($text{'ldap_ModulesConstraints'},
# 		    &ui_textbox("ldap_ModulesConstraints",
# 				undef,
# 				20));
print &ui_table_end();

print &ui_table_start($text{'SOGoUserSource_sql'}, 'id="SQL_options"', 2);
print &ui_table_row(&hlink($text{'sql_viewURL'}, "sql_viewURL"),
		    &ui_textbox("sql_viewURL",
				 'driver://username:password@hostname/database/viewname',
				 60) . '<br/><span>' . $text{database_format} . '</span>');
print &ui_table_row($text{'sql_userPasswordAlgorithm'},
		    &ui_select("sql_userPasswordAlgorithm",
			       "none",
			       [ "none", "md5" ],
			       1,
			       0,
			       0
			       ));
print &ui_table_end();

print &ui_form_end([ [ undef, $text{'create'}, $text{'note_restart'} ] ]);

&ui_print_footer("sources.cgi", $text{'previous_return'});

