#!/usr/bin/perl
#
# sogo-module by Francis Lachapelle <flachapelle@inverse.ca>,
# for webmin by Jamie Cameron

require 'sogo-lib.pl';

error_setup($text{'restart_err'});

&error($err) if ($err = &restart_daemon());

&redirect("index.cgi");

