#!/usr/bin/perl
#
# sogo-module by Francis Lachapelle <flachapelle@inverse.ca>,
# for webmin by Jamie Cameron

require './sogo-lib.pl';

&ReadParse();

#$access{'users'} || &error($text{'user_ecannot'});
&error_setup($text{'delete_err'});

@d = split(/\0/, $in{'d'});
@d || &error($text{'source_enone'});

@sources = &defaults_read_array("SOGoUserSources");
@new_sources = ();
foreach $source (@sources) {
  $s = &string2hash($source);
  push(@new_sources, $source) unless grep(/^$s->{id}$/, @d);
}
&error($text{'source_efound'}) unless (scalar(@new_sources));

&error($text{'SOGoUserSources'}) unless &defaults_write_array("SOGoUserSources", \@new_sources);

&webmin_log("delete", "sources", join(",",@d));
&redirect("sources.cgi");

