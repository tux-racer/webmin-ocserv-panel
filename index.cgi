#!/usr/bin/perl
use strict;
use warnings;
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use URI::Escape;

my $q = CGI->new;

# Ambil dan decode pesan hasil
my $result = $q->param('result') // '';
$result = uri_unescape($result);
my $result_html = $result ne '' ? $q->escapeHTML($result) : '';

# Baca daftar user dari file passwd
my @users;
my $passwd_file = "/etc/ocserv/passwd";
if (-e $passwd_file) {
    open(my $fh, '<', $passwd_file);
    while (my $line = <$fh>) {
        chomp $line;
        my ($username) = split(':', $line);
        push @users, $username if $username;
    }
    close($fh);
}

# Cetak HTML
print $q->header(-type => 'text/html', -charset => 'utf-8');
print <<'HTML_HEAD';
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Ocserv Admin Panel</title>
    <link href="/ocserv-panel/assets/css/bootstrap.min.css" rel="stylesheet">
    <link href="/ocserv-panel/assets/css/bootstrap-icons.css" rel="stylesheet">
    <link href="/ocserv-panel/assets/css/sweetalert2.min.css" rel="stylesheet">
    <style>
        body { background: linear-gradient(135deg, #e0e7ff 0%, #f8fafc 100%); min-height: 100vh; }
        .main-card { border-radius: 1.5rem; box-shadow: 0 8px 32px rgba(31,38,135,0.15); background: rgba(255,255,255,0.95);}
        .panel-header { background: linear-gradient(90deg, #6366f1 0%, #60a5fa 100%); color: #fff; padding: 2rem 2rem 1rem; border-radius: 1.5rem 1.5rem 0 0; }
        .btn i { margin-right: 6px;}
        .form-label { font-weight: 500;}
    </style>
    <script src="/ocserv-panel/assets/js/sweetalert2.all.min.js"></script>
</head>
<body>
<div class="container py-5">
    <div class="main-card mx-auto" style="max-width: 1200px;">
        <div class="panel-header d-flex justify-content-between align-items-center">
            <h1 class="mb-0"><i class="bi bi-shield-lock-fill fs-2 me-2"></i>Ocserv Admin Panel</h1>
        </div>
        <div class="row g-0">
            <!-- Form Input -->
            <div class="col-md-7 p-4">
                <form action="add_user.cgi" method="post" class="card p-4 bg-transparent border-0 shadow-none mb-4">
                    <div class="mb-3">
                        <label class="form-label" for="username">Username</label>
                        <input class="form-control" type="text" name="username" id="username" placeholder="Masukkan username baru">
                    </div>
                    <div class="mb-3">
                        <label class="form-label" for="password">Password</label>
                        <input class="form-control" type="password" name="password" id="password" placeholder="Masukkan password">
                    </div>
                    <div class="d-grid gap-2">
                        <button class="btn btn-success" type="submit"><i class="bi bi-person-plus"></i>Tambah User</button>
                        <a class="btn btn-primary" href="show_users.cgi"><i class="bi bi-people"></i>Cek User Online</a>
                    </div>
                </form>
HTML_HEAD

# Output hasil jika ada
if ($result_html) {
    print <<HTML_RESULT;
                <div class="card p-3 shadow mb-4 bg-light border-0">
                    <h5 class="mb-3"><i class="bi bi-terminal"></i> Output:</h5>
                    <pre class="mb-0">$result_html</pre>
                </div>
HTML_RESULT
}

print <<'HTML_USER_LIST';
            </div>
            <!-- Daftar User -->
            <div class="col-md-5 p-4 border-start">
                <div class="card p-3 shadow mb-4 bg-light border-0">
                    <h5 class="mb-3"><i class="bi bi-people-fill"></i> Daftar User:</h5>
                    <ul class="list-group list-group-flush">
HTML_USER_LIST

# Tampilkan semua user
foreach my $user (@users) {
    my $safe_user = CGI::escapeHTML($user);
    print <<HTML;
        <li class="list-group-item d-flex justify-content-between align-items-center">
            <span><i class="bi bi-person-circle text-primary me-2"></i>$safe_user</span>
            <div class="d-flex gap-2">
                <form action="delete_user.cgi" method="post" class="m-0 d-inline-block delete-user-form">
                    <input type="hidden" name="username" value="$safe_user">
                    <button type="submit" class="btn btn-danger btn-sm btn-delete-user" data-username="$safe_user" title="Hapus">
                        <i class="bi bi-person-dash me-0"></i>
                    </button>
                </form>
                <form action="disconnect_user.cgi" method="post" class="m-0 d-inline-block">
                    <input type="hidden" name="username" value="$safe_user">
                    <button type="submit" class="btn btn-warning btn-sm text-white" title="Disconnect">
                        <i class="bi bi-plug text-dark me-0"></i>
                    </button>
                </form>
                <form action="show_user.cgi" method="post" class="m-0 d-inline-block">
                    <input type="hidden" name="username" value="$safe_user">
                    <button type="submit" class="btn btn-info btn-sm text-white" title="Detail">
                        <i class="bi bi-person-badge me-0"></i>
                    </button>
                </form>
            </div>
        </li>
HTML
}

print <<'HTML_END';
                    </ul>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
document.querySelectorAll('.btn-delete-user').forEach(function(btn) {
    btn.addEventListener('click', function(e) {
        e.preventDefault();
        const form = btn.closest('form');
        const username = btn.getAttribute('data-username');
        Swal.fire({
            title: 'Hapus User?',
            text: 'Yakin ingin menghapus user "' + username + '"?',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Ya, hapus!',
            cancelButtonText: 'Batal'
        }).then((result) => {
            if (result.isConfirmed) {
                form.submit();
            }
        });
    });
});
</script>
</body>
</html>
HTML_END
