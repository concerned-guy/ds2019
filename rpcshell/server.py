from SimpleXMLRPCServer import SimpleXMLRPCServer
import getpass
import os
import subprocess

lock = False
user = getpass.getuser()
home = os.path.expanduser('~')
cwd = {}
server = SimpleXMLRPCServer(('localhost', 8080), allow_none=True)
server.register_introspection_functions()
server.register_multicall_functions()

class RPCShell:

    def shell(self, id):
        if id in cwd:
            return False
        cwd[id] = home          # we start at home dir

    def prompt(self, id):
        return '%s [%s] > ' % (user, cwd[id])

    def execute(self, id, cmd):
        global lock
        if id not in cwd:
            return False
        if lock:
            return 'Another process is running, please wait...\n'
        lock = True
        if cmd == 'cd':
            # back to home
            cwd[id] = home
        if cmd[:3] == 'cd ':
            # change working directory
            tmp = cmd.split() + ['']
            if tmp[1] == '':
                cwd[id] = home
            else:
                try:
                    os.chdir(tmp[1])
                    cwd[id] = os.getcwd()
                    lock = False
                    return ''
                except OSError:
                    lock = False
                    return 'Invalid directory.\n'
        os.chdir(cwd[id])
        try:
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
        except:
            output = 'There was an error executing that command, try again.\n'
        lock = False
        return output

server.register_instance(RPCShell())

if __name__ == '__main__':
    print 'listening for RPC requests on localhost:8080'
    server.serve_forever()
