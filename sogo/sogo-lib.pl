# sogo-lib.pl
#
# sogo-module by Francis Lachapelle <flachapelle@inverse.ca>,
# for webmin by Jamie Cameron

use WebminCore;
&init_config();

# $sogo_version / dpkg -s sogo | fgrep Version:

sub defaults_read
{
  my $param = shift;
  my $cmd = 'su - ' . $config{'sogo_user'} . ' -c "' .$config{'gnustep_defaults_command'} . " read " . $config{'gnustep_domain'} . " " . $param . '"';
  #warn ('[defaults_read] ' . $cmd);
  my $out = &backquote_logged("$cmd 2>&1 </dev/null", 1);
  my $ex = $?;
  unless ($ex) {
    if (length($param)) {
      if ($out =~ m/$config{'gnustep_domain'} $param (.+)/s) {
	$out = $1;
      }
      else {
	warn ('[defaults_read] Error (' . $param . '): Unknown output (' . $out . ')');
      }
    }
    chomp($out);
  }
  else {
    warn ('[defaults_read] Warning (' . $param. '): ' . $out);
    $out = "";
  }
  #warn ('[defaults_read] ' . "$param = |$out|");
  return $out;
}

sub defaults_read_bool
{
  my $param = shift;
  my $default = shift || 0;
  my $v = &defaults_read($param);
  my $out = 0;
  if ($v =~ /^$/) {
    $out = $default;
  }
  elsif ($v =~ /^yes$/i) {
    $out = 1;
  }

  return $out;
}

sub defaults_read_array
{
  my $param = shift;
  my $v = &defaults_read($param);
  my @a = &string2array($v);

#  $v =~ s/'?\((.*)\)'/$1/s;
#  #$v =~ s/\n//gs;
#  while ($v =~ m/\s*(([^,"]+?(".+?")?[^,"]+?)+)(,|\s*$)/g) {
#    push (@a, $1);
#  }

  return @a;
}

sub defaults_write
{
  my $param = shift;
  my $value = shift; $value =~ s/"/\\"/g;

  my $backup = &defaults_read("");
  my $operation = length($value)?"write":"delete";

  my $domain = $config{'gnustep_domain'};
  my $cmd = 'su - ' . $config{'sogo_user'} . ' -c "' . $config{'gnustep_defaults_command'} . " $operation $domain $param $value\"";
  #warn "$cmd";
  my $out = &backquote_logged("$cmd 2>&1 </dev/null", 1);
  my $ex = $?;
  if ($ex) {
    warn ('[defaults_write] Error (' . $param . '): ' . $out);
    my @params;
    while ($backup =~ m/^(.+)$/mg) {
      $line = $1;
      if ($line =~ m/^($domain .*)/) {
	push(@params, $buf) if ($buf);
	$buf = $1;
      }
      else {
	$buf .= $line;
      }
    }
    push(@params, $buf) if ($buf);
    foreach $param (@params) {
      $cmd = $config{'gnustep_defaults_command'} . " -u " . $config{'sogo_user'} . " write " . $param;
      &backquote_logged("$cmd 2>&1 </dev/null", 1);
    }
    warn ('[defaults_write] Backup restored.');
  }

  return ($ex == 0);
}

sub defaults_write_array
{
  my $param = shift;
  my $values = shift;
  #my @v = map(chomp, @{$values})

  return &defaults_write($param, "'(" . join(",", @{$values}) . ")'");
}

sub defaults_write_add_to_array
{
  my $param = shift;
  my $v = shift;
  my @values = &defaults_read_array($param);
  push(@values, $v);
  
  return &defaults_write_array($param, \@values);
  #&defaults_write($param, "'(" . join(",", @values) . ")'");
}

sub init_daemon
{
  my $command = shift;
  my $result = undef;
  if (length ($config{'init_command'})) {
    my $out = &backquote_logged("$config{'init_command'} $command 2>&1");
    if ($? || $out =~ /failed|error/i) {
      $result = "<pre>$?\n$out</pre>";
    }
  }
  else {
    $result = "Init command is not defined.";
  }

  return $result;
}

sub restart_daemon
{
  return &init_daemon("restart");
}

sub start_daemon
{
  return &init_daemon("start");
}

sub stop_daemon
{
  return &init_daemon("stop");
}

sub status_daemon
{
  my $result = undef;
  if (length ($config{'init_command'})) {
    my $out = &backquote_logged("$config{'init_command'} status 2>&1");
    $result = $?;
  }
  else {
    $result = -1;
  }

  return $result;
}

sub format_hash
{
  my $v = shift;
  $v =~ s/^\{(.+)\}\n?$/$1/s;
  $v =~ s/^\s+//gm;

  return $v;
}

sub string2hash
{
  my $v = shift;
  my %h = {};
  while ($v =~ m/(\S+)\s*=\s+([^;]+);/msg) {
    #warn ("[string2hash] |$1| = |$2|\n");
    my ($k, $s) = ($1, $2);
    $s =~ s/^"(.*)"$/$1/;
    $h{$k} = $s; # case sensitive
  }
  
  return \%h;
}

sub string2array
{
  my $v = shift;
  my @a;
  $v =~ s/'?\((.*)\)'?/$1/s;
  while ($v =~ m/\s*(([^,"]+?(".+?")?[^,"]+?)+)(,|\s*$)/g) {
    push (@a, $1);
  }

  return @a;
}

sub hash2string
{
  my $h = shift;
  my @a = ();
  foreach $key (keys %{$h}) {
    $v = $h->{$key};
    $v = "\"$v\"" if ($v =~ m/[\s,\"=\;:]/);
    push(@a, "$key = $v;") if (length($v));
  }

  return '{' . join(" ", @a) . '}';
}

sub get_timezones
{
  my @t;
  my $dirname = '/usr/share/zoneinfo/right';
  opendir(DIR, $dirname) or die "can't opendir $dirname: $!";
  while (defined($file = readdir(DIR))) {
    next if ($file =~ m/^\.+/);
    if (-d "$dirname/$file") {
      my $subdirname = "$dirname/$file";
      opendir(SUBDIR, $subdirname) or die "can't opendir $subdirname: $!";
      while (defined($subfile = readdir(SUBDIR))) {
	unless (-d "$subdirname/$subfile") {
	  push(@t, "$file/$subfile");
	}
      }
      close(SUBDIR);
    }
    else {
      push(@t, $file);
    }
  }
  closedir(DIR);
  @t = sort (@t);

  return \@t;
}

# option_radios_freefield(name_of_option, length_of_free_field, [name_of_radiobutton, text_of_radiobutton]+)
# builds an option with variable number of radiobuttons and a free field
# WARNING: *FIRST* RADIO BUTTON *MUST* BE THE DEFAULT VALUE OF POSTFIX
sub option_radios_freefield
{
    my ($name, $length) = ($_[0], $_[1]);

    my $v = &defaults_read($name);
    my $key = $name;

    my $check_free_field = 1;
    
#     my $help = -r &help_file($module_name, "opt_".$name) ?
#       &hlink($text{$key}, "opt_".$name) : $text{$key};
    my $rv;

    # first radio button (must be default value!!)
#     $rv .= &ui_oneradio($name."_def", "__DEFAULT_VALUE_IE_NOT_IN_CONFIG_FILE__",
# 		       $_[2], &if_default_value($name));
# 
#     $check_free_field = 0 if &if_default_value($name);
#     shift;
    
    # other radio buttons
    while (defined($_[2]))
    {
      warn ("$v =? $_[2]\n");
      $rv .= &ui_oneradio($name."_def", $_[2], $_[3], $v eq $_[2]);
      if ($v eq $_[2]) { $check_free_field = 0; }
      shift;
      shift;
    }

    # the free field
#     $rv .= &ui_oneradio($name."_def", "__USE_FREE_FIELD__", undef,
# 		       $check_free_field == 1);
    $rv .= &ui_textbox($name, $check_free_field == 1 ? $v : undef, $length);
    print &ui_table_row($text{$name}, $rv, $length > 20 ? 3 : 1);
}

1;
