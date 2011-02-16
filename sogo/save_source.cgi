#!/usr/bin/perl
#
# sogo-module by Francis Lachapelle <flachapelle@inverse.ca>,
# for webmin by Jamie Cameron

require 'sogo-lib.pl';

&ReadParse();

error_setup($text{'save_err'});

@sources = &defaults_read_array("SOGoUserSources");

# Parse source definition from web form
%s = {};
$s{id}                             = $in{SOGoUserSource_id};
$s{displayName}                    = $in{SOGoUserSource_displayName};
$s{canAuthenticate}                = $in{SOGoUserSource_canAuthenticate} || 'NO';
$s{isAddressBook}                  = $in{SOGoUserSource_isAddressBook} || 'NO';
$s{type}                           = $in{SOGoUserSource_type};

if ($s{type} eq 'ldap') {
  @hostname                        = split(/[\r\n]/, $in{'ldap_hostname'});
  $s{hostname}                     = join(" ", @hostname);
  $s{port}                         = $in{ldap_port};
  $s{encryption}                   = $in{ldap_encryption} if ($in{ldap_encryption} ne 'None');
  $s{CNFieldName}                  = $in{ldap_CNFieldName};
  $s{IDFieldName}                  = $in{ldap_IDFieldName};
  $s{UIDFieldName}                 = $in{ldap_UIDFieldName};
  $s{MailFieldNames}               = '(' . join(", ", split(/\r?\n/, $in{ldap_MailFieldNames})) . ')' if ($in{ldap_MailFieldNames}); 
  $s{IMAPHostFieldName}            = $in{ldap_IMAPHostFieldName};
  $s{baseDN}                       = $in{ldap_baseDN};
  $s{filter}                       = $in{ldap_filter};
  $s{scope}                        = $in{ldap_scope};
  $s{bindDN}                       = $in{ldap_bindDN};
  $s{bindPassword}                 = $in{ldap_bindPassword};
  $s{bindFields}                   = '(' . join(", ", split(/\r?\n/, $in{ldap_bindFields})) . ')' if ($in{ldap_bindFields});
  $s{SOGoLDAPContactInfoAttribute} = $in{SOGoLDAPContactInfoAttribute};
  $s{SOGoLDAPQueryLimit}           = $in{SOGoLDAPQueryLimit};
  $s{SOGoLDAPQueryTimeout}         = $in{SOGoLDAPQueryTimeout};
  $s{passwordPolicy}               = $in{ldap_passwordPolicy} || 'NO';
}
elsif ($s{type} eq 'sql') {
  $s{viewURL}                      = $in{sql_viewURL};
  $s{userPasswordAlgorithm}        = $in{sql_userPasswordAlgorithm};
  $s{MailFieldNames}               = '(' . join(", ", split(/\r?\n/, $in{sql_MailFieldNames})) . ')' if ($in{sql_MailFieldNames});
}

if ($in{id}) {
  # Modify an existing source
  for (my $i; $i < scalar(@sources); $i++) {
    my $source = $sources[$i];
    my $sh = &string2hash($source);
    if ($sh->{id} eq $in{id}) {
      # If the password was not specified, keep the previous one
      $s{bindPassword} = $sh->{bindPassword} if ($in{ldap_bindPassword} eq '');
      $definition = &hash2string(\%s);
      $sources[$i] = $definition;
    }
  }
}
else {
  # Create a new source
  $definition = &hash2string(\%s);
  push(@sources, $definition);
}

warn "SOURCES = ",join("\n", @sources),"\n";
&error($text{'SOGoUserSources'}) unless &defaults_write_array("SOGoUserSources", \@sources);
&webmin_log($in{id}?"modify":"create", "source", $s{id});

&redirect("sources.cgi");

