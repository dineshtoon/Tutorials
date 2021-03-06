#!/usr/bin/python
"""
--------------------------------------------------------------------------
Python script to send SMS using services like Way2SMS, FullOnSMS, Site2SMS
--------------------------------------------------------------------------
This script basically simulates a login, just as you would, while sending
the SMS using these websites. But, saves you time by automating stuff, plus
you can do other cool stuff with this script.

DISCLAIMER
The main intention for this script is for educational purposes only.

For clarifications, contace me at
@dhruvbaldawa on twitter
Dhruv Baldawa on Facebook/Google+

REFERENCES
http://docs.python.org/library/cookielib.html#examples
http://docs.python.org/library/urllib2.html
http://code.google.com/p/android-scripting/wiki/ApiReference

"""

import cookielib
import urllib2
from getpass import getpass # for unix only, comment this line if using in windows
import sys
from urllib import urlencode
import android

droid = android.Android()

# Default initializations (saves time)
username = None
password = None
message = None
number = None
TOTAL = 260

# Initializing some "so-called" constants
CONNECTION_ERROR = -1
SUCCESS = 1

def login(username, password, opener):
  '''
  This method takes care of logging onto the website
  '''
  #Logging into the SMS Site
  url = 'http://www.site2sms.com/auth.asp'
  url_data = urlencode({'txtCCode':'91',
                            'userid':username,
                            'Password':password,
                            'Submit':'Login'})
  # debug message
  # print url_data
  try:
  	usock = opener.open(url, url_data)
  	# debug message
  	# print usock.read()
  except IOError:
  	return CONNECTION_ERROR
  return SUCCESS

def sms_send(number, message, opener):
  # SMS sending
  send_sms_url = 'http://www.site2sms.com/user/send_sms_next.asp'
  send_sms_data = urlencode({'txtCategory':'40', 
                                  'txtGroup':'0',
                                  'txtLeft': len(message) - TOTAL, 
                                  'txtMessage': message, 
                                  'txtMobileNo': number,
                                  'txtUsed':len(message)})
  
  opener.addheaders = [('Referer','http://www.site2sms.com/user/send_sms.asp')]
  
  print "Message Length: ", len(message)
  
  try:
  	sms_sent_page = opener.open(send_sms_url,send_sms_data)
  except IOError:
  	return CONNECTION_ERROR
  return SUCCESS



# Take the user input
if username is None: username = droid.dialogGetInput('Username','Enter username')
# getpass() method takes shell input, without displaying the password
# however, it may not work in windows, so use the following line in 
# windows.
#
#if password is None: password = raw_input("Enter password: ")
if password is None: password = droid.dialogGetPassword('Password','Enter password')
if number is None: number = droid.dialogGetInput('Mobile Number','Enter Number')
if message is None: message = droid.dialogGetInput('Message','Enter Message')

# CookieJar for automatic handling of cookies
# For more information on cookielib
# http://docs.python.org/library/cookielib.html#examples
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

# To fool the website as if a Web browser is visiting the site
opener.addheaders = [('User-Agent','Mozilla/5.0 (Ubuntu; X11; Linux x86_64; rv:8.0) Gecko/20100101 Firefox/8.0')]

# Send the SMS
return_code = login(username, password, opener)

if return_code == CONNECTION_ERROR:
  droid.makeToast("Error while logging in. Check your internet connection")
  sys.exit(1)
elif return_code == SUCCESS:
  droid.makeToast("Logged in successfully.")

return_code = sms_send(number, message, opener)

if return_code == CONNECTION_ERROR:
  droid.makeToast("Error while sending SMS. Check your internet connection")
elif return_code == SUCCESS:
  droid.makeToast("SMS Sent successfully.")

