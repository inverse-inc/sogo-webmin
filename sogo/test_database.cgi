#!/usr/bin/perl
#
# sogo-module by Francis Lachapelle <flachapelle@inverse.ca>,
# for webmin by Jamie Cameron

require 'sogo-lib.pl';

&ReadParse();

popup_header($text{"Tester"});
print ui_subheading($text{"Database Access"});

error_setup($text{'module_err'});
eval "use DBI";
popup_error("Please install the DBI Perl module.") if ($@);
popup_error($text{'parameter_err'}) unless ($in{url});

# postgresql://sogo:sogo@127.0.0.1:5432/sogo/sogo_user_profile
if ($in{url} =~ m/^([^:]+):\/\/([^:]+):([^@]+)@([^:\/]+)(?::(\d+))?\/([^\/]+)\/(\S+)/) {
  ($driver, $username, $password, $hostname, $port, $database, $table)
    = ($1, $2, $3, $4, $5, $6, $7);
  if ($driver =~ m/postgresql/) {
    $driver = 'Pg';
    $url = 'dbi:Pg:dbname=%s;host=%s;port=%s';
    $port = '5432' unless ($port);
  }
  elsif ($driver =~ m/mysql/) {
    $driver = 'mysql';
    $url = 'dbi:mysql:database=%s;host=%s;port=%s';
    $port = '3306' unless ($port);
  }
  elsif ($driver =~ m/oracle/) {
    $driver = 'Oracle';
    $url = 'dbi:Oracle:sid=%s;host=%s;port=%s';
    $port = '1521' unless ($port);
  }

  eval {
    $drh = DBI->install_driver($driver);
  };
  popup_error("Driver $driver not installed") if ($@);
  local $dbh = DBI->connect(sprintf($url, $database, $hostname, $port), $username, $password, { PrintError => 0 });
  if ($dbh) {
    print "<h3>$text{success}</h3>";
  }
  else {
    popup_error($text{failed} . ': ' . $DBI::errstr);
  }
}

popup_footer();
