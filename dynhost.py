#!/usr/local/bin/python2.7

#
# CONFIG GOES HERE
#
import os
import os.path as p
import re
import urllib2
import time
import subprocess
import sys

host = "hostname.net"
login = "login"
password = "password"

PATH_APP = "/usr/local/dynhost"
PATH_LOG = p.join(PATH_APP, "log")
OLD_IP = p.join(PATH_APP, "old_ip")

#
# CONFIG END
#

# prevent error when ipcheck.err exists
try:
   os.unlink( p.join(PATH_APP, "ipcheck.err"))
except:
   pass

logfile = open(PATH_LOG, "a+")
print("Logging in "+PATH_LOG)

def Log(msg):
   s = "%s | %s\n"%(time.strftime("%d/%m/%Y %H:%M:%S"), msg) 
   logfile.write(s)
   print(s)
   
if __name__=="__main__":

   page = urllib2.urlopen("http://monip.org").read()
   res = re.search("IP : (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", page, re.DOTALL)

   if not res:
      Log("Couldn't find an ip")

   else:
      ip = res.groups(0)[0]
      Log("Get new ip : %s"%ip)

      try:
         oldip = open(OLD_IP, "r").read()
      except:
         oldip = ""

      if ip == oldip:
         Log("IP hasn't changed, old=%s, new=%s"%(oldip, ip))
      else:
         Log("IP has changed, old=%s, new=%s"%(oldip, ip))

         args = ["%s %s %s %s %s %s %s"%(p.join(PATH_APP, "ipcheck.py"), "-v", "-a", ip, login, password, host)]
         Log("Calling "+" ".join(args))
         st = subprocess.call(" ".join(args), shell=True, stdout=logfile)
         fip = open(OLD_IP, "w")
         fip.write(ip)
         fip.close()
         Log("Writing ip=%s to %s"%(ip, OLD_IP))
     
      logfile.close()

