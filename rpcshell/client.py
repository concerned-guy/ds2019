from __future__ import print_function
import xmlrpclib
import os

pid = os.getpid()
url = 'http://localhost:8080'
s = xmlrpclib.ServerProxy(url)
print('Welcome to remote shell at ' + url)
s.shell(pid)
while True:
    print(s.prompt(pid), end='')
    cmd = raw_input()
    print(s.execute(pid, cmd), end='')

