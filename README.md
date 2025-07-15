This is webmin module for Ocserv or openconnect vpn for user manager, add user, remove user, show all user, show online user and disconnect

copy ocserv-panel
to
/usr/share/webmin

install libcgi-pm-perl
apt install libcgi-pm-perl

restart
systemctl restart webmin

check

perl /usr/share/webmin/ocserv-panel/index.cgi
