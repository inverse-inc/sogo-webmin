#!/usr/bin/perl
#
# sogo-module by Francis Lachapelle <flachapelle@inverse.ca>,
# for webmin by Jamie Cameron

require 'sogo-lib.pl';

&ReadParse();

popup_header($text{"Tester"});
print ui_subheading($text{"LDAP Access"});

error_setup($text{'module_err'});
eval "use Net::LDAP";
popup_error("Please install the Net::LDAP Perl module.") if ($@);  
popup_error($text{'parameter_err'}) unless ($in{id});

@sources = &defaults_read_array("SOGoUserSources");
$definition = undef;
for (my $i; $i < scalar(@sources) && !defined($definition); $i++) {
  my $source = $sources[$i];
  my $sh = &string2hash($source);
  if ($sh->{id} eq $in{id}) {
    $definition = $sh;
  }
}
popup_error($text{'source_efound'}) unless ($definition);

if ($definition->{encryption}) {
  eval "use IO::Socket::SSL";
  popup_error("Please install the IO::Socket::SSL Perl module.") if ($@);  
}

if ($definition->{encryption} eq 'SSL') {
  $host = 'ldaps://' . $definition->{hostname};
}
else {
  $host = $definition->{hostname};
}
$ldap = Net::LDAP->new($host, version => 3);
if ($ldap) {
  if ($definition->{encryption} eq 'STARTTLS') {
    $msg = $ldap->start_tls(verify => 'none', sslversion => 'tlsv1');
    popup_error($text{failed} . ': ' . $msg->error()) if ($msg->is_error());
  }
  if ($definition->{bindDN} && $definition->{bindPassword}) {
    $msg = $ldap->bind($definition->{bindDN}, password => $definition->{bindPassword});
    popup_error($text{failed} . ': ' . $msg->error()) if ($msg->is_error());
  }
  print "<h3>$text{success}</h3>";
}
else {
  popup_error($text{failed} . ': ' . $@);
}

popup_footer();
