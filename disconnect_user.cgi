#!/usr/bin/perl
use strict;
use warnings;
use CGI;
use WebminCore;
init_config();

my $q = CGI->new;
my $username = $q->param('username');
$username =~ s/[^a-zA-Z0-9._-]//g;

my $output = `sudo /usr/bin/occtl disconnect user $username 2>&1`;

#print $q->header();
#print "<pre>$output</pre>";
#print "<a href='index.cgi'> Kembali</a>";

#my $encoded = $q->escapeHTML($output);
#print $q->redirect("index.cgi?result=$encoded");

my $encoded = $q->escape($output);
print $q->redirect("index.cgi?result=$encoded");
