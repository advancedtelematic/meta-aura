#!/usr/bin/python

'''
Helper script to generate a pianobar config and start Patiobar, for starting it
as a systemd service.

Needs some environment variables set:

PIANOBAR_FIFO - Script will delete and then re-create the fifo
PANDORA_USER - self-explanatory
PANDORA_PASSWORD - self-explanatory
PATIOBAR_DIR - the fully qualified location of your patiobar directory
PIANOBAR_PROXY - Give a proxy address and port to set a proxy, set as "auto" to
automatically find an open US proxy, or leave blank/unset for no proxy 
'''

import os
import httplib
import urllib2
import sys
import random
import time
import subprocess
from bs4 import BeautifulSoup as BS

def wait_for_network():
  while True:
    try:
      response = urllib2.urlopen('http://google.com',timeout=1)
      return
    except Exception:
      pass
    time.sleep(5)
    print "Still waiting..."

def get_proxy_list():
  # setting up the connecting using get request
  conn = httplib.HTTPSConnection("www.sslproxies.org")
  conn.request("GET", "/")
  
  # getting the response and storing it in data
  response = conn.getresponse()
  data = response.read()
  # applying beautifulsoup for parsing
  soup = BS(data,"html.parser")
  # parsing the table for the needed info
  table = soup.find('tbody')
  rows = table.findAll('tr')
  retval=[]
  
  for tr in rows:
    cols = tr.findAll('td')
    # parsing and storing data in each row
    IP_Address,Port,Code_Country,Country,Type_proxy,Google,https,LastCheck = [c.text for c in cols]
    # displaying string along with needed infos
    proxy = IP_Address+":"+Port
    if Country == "United States":
      retval.append(proxy)
      print "Found " + proxy + ", " + Type_proxy
  
  if len(retval) == 0:
    raise Exception("Proxy list could not be retrieved or was empty")
  return retval

def test_proxy(p):
  try:
    print "Trying " + p + "...",
    urllib2.install_opener(
      urllib2.build_opener(
        urllib2.ProxyHandler({'http':"http://"+p,'https':"http://"+p})
      )
    )
    urllib2.urlopen("https://google.com",timeout = 2)
    print  "success!"
    return True
  except Exception:
    print "connection failed :-("
    return False
    pass

def get_proxy():
  print "Getting proxy list..."
  proxylist = get_proxy_list() 
  random.shuffle(proxylist)
  for prox in proxylist:
    if test_proxy(prox):
      return prox

  raise Exception("No working proxies found")

def generate_config():
  config_path = os.environ["HOME"] + "/.config/pianobar"
  if not os.path.exists(config_path):
    os.makedirs(config_path)

  if "PIANOBAR_FIFO" in os.environ:
    if os.path.exists(os.environ["PIANOBAR_FIFO"]):
      os.remove(os.environ["PIANOBAR_FIFO"])
    fifo_line = "fifo = " + os.environ["PIANOBAR_FIFO"] + "\n"
    os.mkfifo(os.environ["PIANOBAR_FIFO"])

  if "PANDORA_USER" in os.environ:
    user_line = "user = " + os.environ["PANDORA_USER"] + "\n"
  else:
    print "Error: environment variable PANDORA_USER must be set."
    sys.exit(1)

  if "PANDORA_PASSWORD" in os.environ:
    password_line = "password = " + os.environ["PANDORA_PASSWORD"] + "\n"
  else:
    print "Error: environment variable PANDORA_PASSWORD must be set."
    sys.exit(1)

  global patiobar_dir
  if "PATIOBAR_DIR" in os.environ:
    patiobar_dir = os.environ["PATIOBAR_DIR"]
  else:
    patiobar_dir = os.environ["PWD"]
  event_command_line = "event_command = " + patiobar_dir + "/eventcmd.sh\n"

  if "PIANOBAR_PROXY" in os.environ:
    if os.environ["PIANOBAR_PROXY"] == "auto":
      try:
        pianobar_proxy_line = "control_proxy = " + get_proxy() + "\n"
      except Exception:
        print "Error finding a proxy, leaving proxy blank."
        pianobar_proxy_line = ""
        pass
    else:
      pianobar_proxy_line = "control_proxy = " + os.environ["PIANOBAR_PROXY"] + "\n"
  else:
    pianobar_proxy_line = ""

  audio_quality_line = "audio_quality = high\n"

  if os.path.isfile(config_path + "/config"):
    os.rename(config_path + "/config",config_path + "/config.old")

  with open(config_path + "/config","w") as f:
    f.write(fifo_line + user_line + password_line + event_command_line + pianobar_proxy_line + audio_quality_line)

def main():
  print "Waiting for network to come online..."
  print "Killing any existing pianobar screens..."
  subprocess.call("screen -ls | grep pianobar | cut -d. -f1 | awk '{print $1}' | xargs kill > /dev/null",shell=True)
  print "Killing any existing patiobar screens..."
  subprocess.call("screen -ls | grep patiobar | cut -d. -f1 | awk '{print $1}' | xargs kill > /dev/null",shell=True)
  wait_for_network()
  print "Generating pianobar config file..."
  generate_config()
  time.sleep(1)
  global patiobar_dir
  print "Starting patiobar on port 3000..."
  subprocess.call("screen -dmS patiobar node " + patiobar_dir + "/index.js",shell=True)
  print "Done!"
  

if __name__ == '__main__':
    main()
