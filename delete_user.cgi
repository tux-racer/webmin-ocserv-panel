#!/usr/bin/perl
use strict;
use warnings;
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use URI::Escape;
use WebminCore;

&init_config;

my $q = CGI->new;

# Ambil username dari input
my $username = $q->param('username') // '';
$username =~ s/[^a-zA-Z0-9._-]//g;

# Validasi sederhana
if (!$username) {
    my $msg = uri_escape("Error: Username tidak valid atau kosong.");
    print $q->redirect("index.cgi?result=$msg");
    exit;
}

# Jalankan perintah penghapusan user
my $output = `sudo /usr/bin/ocpasswd -d -c /etc/ocserv/passwd $username 2>&1`;

# Tambahan permission fix (opsional)
$output .= `sudo chmod 644 /etc/ocserv/passwd 2>&1`;

# Jika tidak ada output, beri pesan default
$output ||= "User '$username' berhasil dihapus.";

# Encode output untuk URL
my $encoded = uri_escape($output);

# Redirect ke halaman utama dengan output sebagai result
print $q->redirect("index.cgi?result=$encoded");
