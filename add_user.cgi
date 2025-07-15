#!/usr/bin/perl
use strict;
use warnings;
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use URI::Escape;
use WebminCore;

&init_config;
my $q = CGI->new;

# Ambil input dari form
my $username = $q->param('username') // '';
my $password = $q->param('password') // '';

# Validasi input kosong
if (!$username || !$password) {
    my $msg = uri_escape("Error: Username atau password kosong.");
    print $q->redirect("index.cgi?result=$msg");
    exit;
}

# Validasi username agar aman
if ($username !~ /^[a-zA-Z0-9_.-]+$/) {
    my $msg = uri_escape("Error: Username tidak valid (hanya huruf, angka, titik, strip, underscore).");
    print $q->redirect("index.cgi?result=$msg");
    exit;
}

# Periksa apakah binary expect ada
my $expect_bin = `which expect`;
chomp($expect_bin);
if (!$expect_bin || !-x $expect_bin) {
    my $msg = uri_escape("Error: 'expect' tidak ditemukan di sistem.");
    print $q->redirect("index.cgi?result=$msg");
    exit;
}

# Tulis skrip expect ke file sementara
my $expect_script = "/tmp/ocpasswd_$username.expect";
open(my $fh, '>', $expect_script) or die "Tidak bisa menulis ke $expect_script: $!";
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

# Jalankan skrip expect dan ambil output
my $output = `$expect_script 2>&1`;
unlink $expect_script;

# Redirect ke index.cgi dengan output sebagai result
my $encoded = uri_escape($output);
print $q->redirect("index.cgi?result=$encoded");
