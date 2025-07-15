#!/usr/bin/perl
use strict;
use warnings;
use lib $ENV{'WEBMIN_LIB'};
use WebminCore;
&init_config;


my $output = `sudo /usr/bin/occtl show users 2>&1`;

print "Content-type: text/html\n\n";
print "<pre>$output</pre>";
print "<a href='index.cgi'>← Kembali</a>";
