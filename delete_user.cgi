#!/usr/bin/perl
use strict;
use warnings;
use CGI;
use WebminCore;
init_config();

my $q = CGI->new;
my $username = $q->param('username');
$username =~ s/[^a-zA-Z0-9._-]//g;

my $output = `sudo /usr/bin/ocpasswd -d -c /etc/ocserv/passwd $username 2>&1`;
$output .= `sudo chmod 644 /etc/ocserv/passwd`;

print $q->header();
print "<pre>$output</pre>";
print "<a href='index.cgi'>← Kembali</a>";
