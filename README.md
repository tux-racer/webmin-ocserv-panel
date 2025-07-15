# webmin module ocserv

This is user manager webmin module for Ocserv or openconnect vpn, add user, remove user, show all user, show online user and disconnect

extract / clone (example ocserv-panel) directory copy to /usr/share/webmin

Requirement pakage
install libcgi-pm-perl on debian apt install libcgi-pm-perl
install expect package on debian apt install expect

restart
systemctl restart webmin

check
perl /usr/share/webmin/ocserv-panel/index.cgi

or
download ocserv-panel.wbm.gz
then
install module for from webmin module

https://github.com/tux-racer/webmin-ocserv-panel/releases

<img width="782" height="474" alt="Screenshot at 2025-07-15 09-30-34" src="https://github.com/user-attachments/assets/84165d2b-e042-48d9-9c36-c9ce7f4864f7" />
