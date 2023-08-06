#!/usr/bin/env python3

import os, sys, multiprocessing, json, socket, ssl, threading, time

import base64

from prompt_toolkit import PromptSession, ANSI
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.completion import NestedCompleter

# ╔───────────────────────────────────────────────────────────────────────╔─╧─╗ 
#╬╡ tools                                                                 │🔨 ╞╬
# ╚───────────────────────────────────────────────────────────────────────╚─╤─╝ 

home = os.path.expanduser('~')

def create_cert(key, cert):
    os.system(f'openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 -keyout {key} -out {cert}')

def directory_exists(d):
    return os.path.isdir(d)

def file_exists(f):
    return os.path.isfile(f)

def create_directory(path):
    os.makedirs(path)

def info(msg):
    print(f'[+] {msg}')

def error(msg):
    print(f'[!] {msg}')

def read_file(f):
    with open(f, 'r') as content:
        return content.read()

def write_file(f, content):
    F = open(f,"w+")
    F.seek(0)
    F.write(content)
    F.truncate()
    F.close()

def read_json(f):
    return json.loads(read_file(f))

def write_json(f, j):
    write_file(f, json.dumps(j))

def read_stdin():
    return sys.stdin.read()

def fred(func, *args):
    '''
    runs a function in a separate thread, returning a Result object.
    - fred.complete() returns True if the task was completed already
    - fred.result()   blocks, returning the result.
    '''
    class Result:
        def __init__(self, target, args):
            self.target       = target
            self.args         = args
            self.result_value = None
            self.completed    = False
            self.lock         = threading.Lock()
            self.thread = threading.Thread(target=self._run_target)
            self.thread.start()
        def _run_target(self):
            with self.lock:
                self.result_value = self.target(*self.args)
                self.completed = True
        def complete(self):
            return self.completed
        def result(self):
            self.thread.join()
            return self.result_value
    return Result(func, args)

class Netbee:
    '''
    simple netcat clone, supports
    tcp, udp, unix and ssl
    '''
    def __init__(self,
                 mode,     # 'listen' or 'connect'
                 protocol, # tcp tcp-ssl udp udp-ssl unix
                 host,     # 0.0.0.0/0 or 0::0/0 or example.com
                 port):    # 0-65535

        port = int(port)
        key  = home + "/.honeypot/key"
        cert = home + "/.honeypot/cert"

        if not file_exists(key) or not file_exists(cert):
            create_cert(key, cert)
        
        if mode == 'listen':
            if protocol.startswith('tcp'):
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.sock.bind(("0.0.0.0", port))
                self.sock.listen()
                self.sock, self.client = self.sock.accept()
                print(f'got connec from {self.client[0]} {self.client[1]}')
            if protocol == 'tcp-ssl':
                context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
                context.load_cert_chain(certfile=cert, keyfile=key)
                self.sock = context.wrap_socket(self.sock, server_side=True)
            if protocol == 'udp':
                pass #TODO
            if protocol == 'udp-ssl':
                pass #TODO
            if protocol == 'unix':
                pass #TODO

        if mode == 'connect':
            if protocol.startswith('tcp'):
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((host, port))
            if protocol == 'tcp-ssl':
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                self.sock = context.wrap_socket(self.sock)
            if protocol == 'udp':
                pass #TODO
            if protocol == 'udp-ssl':
                pass #TODO
            if protocol == 'unix':
                pass #TODO

        i = fred(self.recv)
        o = fred(self.send)
        i.result()
        o.result()
        exit(0)
            
    def send(self):
        while True:
            try:
                data = input()+'\n'
                self.sock.sendall(data.encode())
            except: return None

    def recv(self):
        while True:
            try:
                data = self.sock.recv(1024)
                if not data:
                    break
                sys.stdout.write(data.decode())
                sys.stdout.flush()
            except: return None

        

# ╔───────────────────────────────────────────────────────────────────────╔─╧─╗ 
#╬╡ bee                                                                   │ 🐝╞╬
# ╚───────────────────────────────────────────────────────────────────────╚─╤─╝ 
#  every bee is a separate process.

class Bee():
    def __init__(self, function, *args, **kwargs):
        self.function     = function
        self.args         = args
        self.kwargs       = kwargs
        self.process      = None
        
    def work(self):
        self.process = multiprocessing.Process(target=self.function, args=self.args, kwargs=self.kwargs)
        self.process.start()

    def result(self, timeout=None):
        if self.process is not None:
            self.process.join(timeout)

    def alive(self):
        if self.process is not None:
            return self.process.is_alive()

    def die(self):
        if self.process is not None:
            self.process.terminate()

    def shell(self):
        pass # TODO

# ╔───────────────────────────────────────────────────────────────────────╔─╧─╗ 
#╬╡ queen                                                                 │ 👑╞╬
# ╚───────────────────────────────────────────────────────────────────────╚─╤─╝ 
# create more bees, enter hive. this is the main manager daemon.

class Queen(Bee):
    def __init__(self):
        pass

# ╔───────────────────────────────────────────────────────────────────────╔─╧─╗ 
#╬╡ hive                                                                  │ 🐝╞╬
# ╚───────────────────────────────────────────────────────────────────────╚─╤─╝ 
#  multiplayer teamserver!

class Hive:
    def __init__(self, honeypot):
        self.honeypot = honeypot
        pass

# ╔───────────────────────────────────────────────────────────────────────╔─╧─╗ 
#╬╡ honeypot                                                              │ 🍯╞╬
# ╚───────────────────────────────────────────────────────────────────────╚─╤─╝ 
#  hacking engine singleton + main shell
#  is basically entry point and manages config and utilities

class IPAddressCompleter(WordCompleter):
    def get_completions(self, document, complete_event):
        text = document.text_before_cursor.lstrip()

        # If the user has entered a partial IP address, suggest the next part.
        ip_parts = text.split('.')
        if len(ip_parts) < 4:
            for i in range(256):
                yield Completion(f'{text}.{i}' if text else str(i), -len(text))

class Honeypot:
    '''main entry point for honeypot.py. holds config and shell.'''
    def __init__(self):
        self.dir          = home + "/.honeypot/"
        self.db_file      = self.dir + "/honey.db"     # the sqlite databse
        self.config_file  = self.dir + "/honey.config" # the json config
        self.mod_dir      = self.dir + "/bee"          # the module directory
        self.history      = self.dir + "/history"      # shell history
        self.prompt       = "🍯 "                      # shell prompt 
        self.hive         = Hive(self)                 # the teamserver
        self.default_conf = {
            "server" : None
        } 

        # init
        print('A')
        if not directory_exists(self.dir):
            info(f'creating .honeypot ({self.dir})')
            create_directory(self.dir)
        if not file_exists(self.config_file):
            info(f'creating new config ({self.config_file})')
            self.config = self.default_conf
            self.save()
        self.config = self.load()
        print('B')

        # shell
        if len(sys.argv) > 1: args = sys.argv[1:]
        else:                 args = None
        self.shell(args)


    def close(self):
        '''cleans up after shell is exited'''
        exit(0)
        
    # 🔧 config get/set values

    def load(self):
        '''load config from file'''
        self.config = read_json(self.config_file)

    def save(self):
        '''save config to file'''
        write_json(self.config_file, self.config)

    def get(self, var):
        '''get a variable's value (from config file)'''
        self.load()
        return self.config.get(var)

    def set(self, var, val):
        '''set a variable to a value (saves to config file)'''
        self.load()
        self.config[var] = val
        self.save()

    # 🍯 honeypot shell

    def shell(self, cmd):
        '''shell with history and completion, also executes cli args'''

        if cmd: # execute cli args like shell would
            self.handle(cmd)
            self.close()
        while True:
            try: cmd = PromptSession(
                history      = FileHistory(self.history),
                auto_suggest = AutoSuggestFromHistory(),
                completer    = NestedCompleter.from_nested_dict({
                    #'use'    : WordCompleter({'omfg':None}),
                    'encode' : {
                        'b16' : None,
                        'b32' : None,
                        'b64' : None,
                        'b85' : None,
                    },
                    'decode' : {
                        'b16' : None,
                        'b32' : None,
                        'b64' : None,
                        'b85' : None,
                    },
                    'spawn'  : None,
                    'listen' : {
                        'tcp'     : None,
                        'tcp-ssl' : None,
                        'udp'     : None,
                        'udp-ssl' : None,
                        'unix'    : None,
                    },
                    'connect' : {
                        'tcp'     : None,
                        'tcp-ssl' : None,
                        'udp'     : None,
                        'udp-ssl' : None,
                        'unix'    : None,
                    },
                    'q'      : None,
                    'exit'   : None,
                })).prompt(ANSI(self.prompt)).split(' ')
            except KeyboardInterrupt: continue
            except EOFError:          break
            self.handle(cmd)

    def handle(self, cmd):
        '''handler for commands given via shell or argv'''
        if cmd[0] == 'use'     : print('TODO')
        if cmd[0] == 'spawn'   : print('TODO')
        if cmd[0] == 'encode'  :
            if cmd[1] == 'b16' : print(base64.b16encode(read_stdin().encode("utf-8")).decode(),end='')
            if cmd[1] == 'b32' : print(base64.b32encode(read_stdin().encode("utf-8")).decode(),end='')
            if cmd[1] == 'b64' : print(base64.b64encode(read_stdin().encode("utf-8")).decode(),end='')
            if cmd[1] == 'b85' : print(base64.b85encode(read_stdin().encode("utf-8")).decode(),end='')
        if cmd[0] == 'decode'  :
            if cmd[1] == 'b16' : print(base64.b16decode(read_stdin().encode("utf-8")).decode(),end='')
            if cmd[1] == 'b32' : print(base64.b32decode(read_stdin().encode("utf-8")).decode(),end='')
            if cmd[1] == 'b64' : print(base64.b64decode(read_stdin().encode("utf-8")).decode(),end='')
            if cmd[1] == 'b85' : print(base64.b85decode(read_stdin().encode("utf-8")).decode(),end='')
        if cmd[0] == 'listen'  : Netbee(*cmd)
        if cmd[0] == 'connect' : Netbee(*cmd)
        if cmd[0] == 'q'       : self.close()
        if cmd[0] == 'exit'    : self.close()

if __name__ == "__main__":
    Honeypot()
