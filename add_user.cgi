#!/usr/bin/perl
use strict;
use warnings;
use lib $ENV{'WEBMIN_LIB'};
use WebminCore;
&init_config;
&ReadParse();  # WAJIB! Untuk mengisi %in dari POST/GET

my $username = $in{'username'};
my $password = $in{'password'};

&header("Add User", "");

if (!$username || !$password) {
    print "<h3>Error: Username or password is missing.</h3>\n";
    &footer();
    exit;
}

# Buat file expect sementara
my $expect_script = "/tmp/ocpasswd_$username.expect";
open(my $fh, '>', $expect_script);
print $fh <<EOF;
#!/usr/bin/expect -f
set timeout 5
spawn sudo /usr/bin/ocpasswd -c /etc/ocserv/passwd $username
expect "Enter password:"
send "$password\\r"
expect "Re-enter password:"
send "$password\\r"
expect eof
EOF

close($fh);
chmod 0755, $expect_script;

# Jalankan
my $output = `expect $expect_script 2>&1`;
unlink $expect_script;

print "<pre>$output</pre>";
print "<p>User <b>$username</b> has been added.</p>";
print "<a href='index.cgi'>← Kembali</a>";
&footer();
