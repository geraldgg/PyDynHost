#!/usr/local/bin/python2.7

#
# CONFIG GOES HERE
#
import ConfigParser
import os
import os.path as p
import re
import smtplib
import urllib2
import time
import subprocess

curdir=p.dirname(__file__)
cfgfile=p.join(curdir, "user.cfg")
if not p.exists(cfgfile):
   print("Couldn't find "+cfgfile)
   exit(1)

c = ConfigParser.ConfigParser()
c.read(cfgfile)
host = c.get("server", "host")
login = c.get("server", "login")
password = c.get("server", "password")
PATH_APP = curdir

sender = c.get("server", "sender")
receiver = c.get("server", "receiver")
smtp = c.get("server", "smtp")

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

         message = """From: %s
         To: %s
         Subject: IP changed

         IP has been changed %s => %s
         """%(sender, receiver, ip, oldip)
         try:
            smtpObj = smtplib.SMTP(smtp)
            smtpObj.sendmail(sender, receiver, message)
            Log("Successfully sent email")
         except Exception, e:
            Log("Error: unable to send email:"+str(e))

      logfile.close()


