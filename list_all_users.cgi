#!/usr/bin/perl

use strict;
use warnings;

use lib $ENV{'WEBMIN_LIB'};
use WebminCore;
&init_config();

my $passwd = "/etc/ocserv/passwd";
open(my $fh, '<', $passwd) or die "Tidak bisa membuka $passwd: $!";
print "Content-type: text/html\n\n";
print "<h3>Daftar User:</h3><ul>";
while (my $line = <$fh>) {
    chomp($line);
    my ($user) = split(":", $line);
    print "<li>$user</li>" if $user;
}
print "</ul><a href='index.cgi'>← Kembali</a>";
