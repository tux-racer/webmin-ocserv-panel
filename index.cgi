#!/usr/bin/perl

use strict;
use warnings;
use lib $ENV{'WEBMIN_LIB'};
use WebminCore;
&init_config;

# Load existing users from passwd file
my $passwd_file = "/etc/ocserv/passwd";
my @users = ();

if (-e $passwd_file) {
    open(my $fh, '<', $passwd_file);
    while (my $line = <$fh>) {
        chomp $line;
        my ($username) = split(':', $line);
        push @users, $username if $username;
    }
    close($fh);
}

print &header();
print "<h1>Ocserv Panel</h1>";

# Form Tambah User

print <<EOF;
<form action="add_user.cgi" method="post">
    <h3>Tambah User</h3>
    <label>Username:</label><br>
    <input type="text" name="username"><br>
    <label>Password:</label><br>
    <input type="password" name="password"><br><br>
    <input type="submit" value="Tambah User">
</form>
EOF


# Form Hapus User
print <<EOF;
<form action="delete_user.cgi" method="post">
    <h3>Hapus User</h3>
    <select name="username">
EOF

foreach my $user (@users) {
    print "<option value=\"$user\">$user</option>\n";
}

print <<EOF;
    </select><br>
    <input type="submit" value="Hapus User">
</form>
EOF

# Form Disconnect User
print <<EOF;
<form action="disconnect_user.cgi" method="post">
    <h3>Disconnect User</h3>
    <select name="username">
EOF

foreach my $user (@users) {
    print "<option value=\"$user\">$user</option>\n";
}

print <<EOF;
    </select><br>
    <input type="submit" value="Disconnect">
</form>
<form action="list_all_users.cgi" method="post">
    <input type="submit" value="List Semua User">
</form>
<form action="show_users.cgi" method="post">
    <input type="submit" value="Lihat User Online">
</form>
EOF

print &footer();
