# PyDynHost

Python script to get dynamic ip, compare it with previous ip, and call ipcheck.py (OVH script) to update ip in DynHost functionality.

Copy user.cfg.tpl to user.cfg, replace the values by the one provided by OVH DynDNS configuration, plus your smpt provider.

Run python dynhost.py using a cron task, adapt the frequency to your needs. I do it every 30 min, it works fine.
