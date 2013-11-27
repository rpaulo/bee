#!/usr/bin/env python 
#
# Copyright (c) 2013 Rui Paulo <rpaulo@FreeBSD.org>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import socket
import threading
import paramiko

class BeeConsole(paramiko.ServerInterface):
    def __init__(self, key=None):
        self.event = threading.Event()

    def set_key(self, key):
        self.priv_key = key

    def generate_key(self):
        return paramiko.DSSKey.generate(bits=1024)

    def init_server(self, port):
        self.sockv4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockv4.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sockv4.bind(('', port))
        self.sockv4.listen(100)
        self.sockv6 = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        self.sockv6.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sockv6.bind(('', port))
        self.sockv6.listen(100)
 
    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if (username == 'root') and (password == 'toor'):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def check_auth_publickey(self, username, key):
        return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username):
        return 'password'

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth,
                                  pixelheight, modes):
        return True

    def _handle_clients(self, socket):
        while 1:
            # XXX error handling
            client, addr = socket.accept()
            t = paramiko.Transport(client)
            t.add_server_key(self.priv_key)
            t.load_server_moduli()
            try:
                t.start_server(server=self)
            except:
                client.close()
                continue
            chan = t.accept(20)
            self.event.wait(10)
            chan.send('test')
            client.close()
    
    def wait_session(self):
        self.v4thread = threading.Thread(target=self._handle_clients, 
                args=(self.sockv4,))
        self.v6thread = threading.Thread(target=self._handle_clients, 
                args=(self.sockv6,))
        self.v4thread.start()
        self.v6thread.start()
        self.v4thread.join()
        self.v6thread.join()

    def stop_session(self):
        pass

if __name__ == "__main__":
    c = BeeConsole()
    c.set_key(c.generate_key())
    c.init_server(port=2200)
    c.wait_session()

