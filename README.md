This is user manager webmin module for Ocserv or openconnect vpn, add user, remove user, show all user, show online user and disconnect

copy ocserv-panel
to
/usr/share/webmin

install libcgi-pm-perl
apt install libcgi-pm-perl

restart
systemctl restart webmin

check

perl /usr/share/webmin/ocserv-panel/index.cgi

or
download ocserv-panel.wbm.gz
then
install module for from webmin module

https://github.com/tux-racer/webmin-ocserv-panel/releases

<img width="1345" height="639" alt="Screenshot at 2025-07-15 11-28-21" src="https://github.com/user-attachments/assets/3977d5e1-82d0-4f07-be80-c4b29e569d22" />


