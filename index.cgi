#!/usr/bin/perl
use strict;
use warnings;
use CGI;
use CGI::Carp qw(fatalsToBrowser);

my $q = CGI->new;
my $result = $q->param('result');

# Load users from /etc/ocserv/passwd
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

print $q->header(-type => 'text/html', -charset => 'utf-8');
print <<'HTML';
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ocserv Admin Panel</title>
    <link href="/ocserv-panel/assets/css/bootstrap.min.css" rel="stylesheet">
    <link href="/ocserv-panel/assets/css/bootstrap-icons.css" rel="stylesheet">
    <link href="/ocserv-panel/assets/css/sweetalert2.min.css" rel="stylesheet">
    <style>
        body { background: linear-gradient(135deg, #e0e7ff 0%, #f8fafc 100%); min-height: 100vh; }
        .main-card { border-radius: 1.5rem; box-shadow: 0 8px 32px 0 rgba(31,38,135,0.15); background: rgba(255,255,255,0.95);}
        .panel-header { background: linear-gradient(90deg, #6366f1 0%, #60a5fa 100%); color: #fff; border-radius: 1.5rem 1.5rem 0 0; padding: 2rem 2rem 1rem 2rem; box-shadow: 0 4px 16px 0 rgba(99,102,241,0.10);}
        .panel-header h1 { font-weight: 700; letter-spacing: 1px;}
        .btn i { margin-right: 6px;}
        .list-group-item { border-radius: 0.5rem; margin-bottom: 0.5rem;}
        .card { border-radius: 1rem;}
        .form-label { font-weight: 500;}
        .btn { font-weight: 500; letter-spacing: 0.5px;}
    </style>
    <script src="/ocserv-panel/assets/js/sweetalert2.all.min.js"></script>
</head>
<body>
<div class="container py-5">
    <div class="main-card mx-auto shadow" style="max-width: 1200px;">
        <div class="panel-header d-flex justify-content-between align-items-center">
            <div class="d-flex align-items-center">
                <i class="bi bi-shield-lock-fill fs-2 me-2"></i>
                <h1 class="mb-0">Ocserv Admin Panel</h1>
            </div>
        </div>
        <div class="row g-0">
            <!-- Left Column: Form & Output -->
            <div class="col-md-7 p-4">
                <form action="add_user.cgi" method="post" class="card p-4 shadow-none border-0 mb-4 bg-transparent">
                    <div class="mb-3">
                        <label for="username" class="form-label">Username</label>
                        <input type="text" name="username" id="username" class="form-control" placeholder="Masukkan username baru">
                    </div>
                    <div class="mb-3">
                        <label for="password" class="form-label">Password (untuk tambah user)</label>
                        <input type="password" name="password" id="password" class="form-control" placeholder="Masukkan password">
                    </div>
                    <div class="d-grid gap-2">
                        <button type="submit" class="btn btn-success"><i class="bi bi-person-plus"></i>Tambah User</button>
                        <a href="show_users.cgi" class="btn btn-primary"><i class="bi bi-people"></i>Cek User Online</a>
                    </div>
                </form>
HTML

# Output log section (outside heredoc)
            if ($result) {
            print <<HTML;
            <div class="card shadow p-3 mb-4 bg-light border-0">
                <h5 class="mb-3"><i class="bi bi-terminal"></i> Output:</h5>
                <pre class="mb-0">$result</pre>
            </div>
HTML
}

print <<HTML;
            </div>
            <!-- Right Column: User List -->
            <div class="col-md-5 p-4 border-start">
                <div class="card shadow p-3 mb-4 bg-light border-0">
                    <h5 class="mb-3"><i class="bi bi-people-fill"></i> Daftar User Terdaftar:</h5>
                    <ul class="list-group list-group-flush">
HTML

foreach my $user (@users) {
    print <<HTML;
    <li class="list-group-item d-flex align-items-center justify-content-between">
        <span>
            <i class="bi bi-person-circle me-2 text-primary"></i>
            $user
        </span>
        <div class="d-flex gap-2">
            <form action="delete_user.cgi" method="post" class="m-0 d-inline-block delete-user-form">
                <input type="hidden" name="username" value="$user">
                <button type="button" class="btn btn-danger btn-sm btn-delete-user" data-username="$user" title="Delete">
                    <i class="bi bi-person-dash me-0"></i>
                </button>
            </form>
            <form action="disconnect_user.cgi" method="post" class="m-0 d-inline-block">
                <input type="hidden" name="username" value="$user">
                <button type="submit" class="btn btn-warning btn-sm text-white" title="Disconnect">
                    <i class="bi bi-plug text-dark me-0"></i>
                </button>
            </form>
            <form action="show_user.cgi" method="post" class="m-0 d-inline-block">
                <input type="hidden" name="username" value="$user">
                <button type="submit" class="btn btn-info btn-sm text-white" title="Info">
                    <i class="bi bi-person-badge me-0"></i>
                </button>
            </form>
        </div>
    </li>
HTML
}

print <<'HTML';
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
HTML
