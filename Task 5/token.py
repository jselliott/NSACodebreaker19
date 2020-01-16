from __future__ import print_function
import urllib2
import base64
import json
import ssl

#Certs for the servers for these challenges can cause issues so we don't worry about verifying them.
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#Put the client ID and secret of one of the test users from README file from task 1 separated by colon
auth = base64.b64encode("test--vhost-1234@terrortime.app:password")

data = "audience=&grant_type=client_credentials&scope=chat"
req = urllib2.Request('https://register.terrortime.app/oauth2/token',data=data)
req.add_header("Authorization","Basic "+auth)
req.add_header("X-Server-Select","oauth")
req.add_header("Content-Type","application/x-www-form-urlencoded")
r = urllib2.urlopen(req,context=ctx)

resp = json.loads(r.read())

print("\n\nGot Access Token:\t\t"+resp['access_token']+"\n\n")
print("You can use this as the password to log into Spark client for task 6a and 6b.\nIt has a 1-hour life, so if you find you aren't able to log in, then run this script again to get a new one.")