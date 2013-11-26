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

import time
import os
import sqlite3

class BeeDatabase:
    def __init__(self):
        self.dbname = "bee.sqlite"
        try:
            os.stat(self.dbname)
        except:
            self.c = self._create_conn()
            self._create_vm_table()
            self._create_pci_slots_table()
        else:
            self.c = self._create_conn()

    def _dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def _create_conn(self): 
        conn = sqlite3.connect(self.dbname)
        conn.row_factory = self._dict_factory
        return conn

    def _create_vm_table(self): 
        self.c.execute('''
            CREATE TABLE vm( 
                name TEXT PRIMARY KEY,
                cdate TEXT,  
                ram INT,
                cpus INT, 
                type TEXT)''')
        self.c.commit()

    def _create_pci_slots_table(self):
        self.c.execute('''
            CREATE TABLE pci_slot(  
                vmname TEXT,
                legacy BOOL,
                slot TEXT,
                driver TEXT,
                config TEXT,
                options TEXT,
                FOREIGN KEY(vmname) REFERENCES vm(name)
                    ON DELETE CASCADE ON UPDATE CASCADE)''')
        self.c.commit()

    def vm_list(self):
        return self.c.execute('SELECT * FROM vm').fetchall()

    def vm_lookup(self, name):
        return self.c.execute('''
            SELECT * from vm WHERE name = "%s"''' % name).fetchone()

    def vm_create(self, name, ram, cpus, vmtype):
        self.c.execute('''
            INSERT INTO vm(cdate, name, ram, cpus, type)
            VALUES('%s', '%s', '%d', '%d', '%s')''' %
            (time.ctime(), name, ram, cpus, vmtype))
        self.c.commit()

    def vm_add_pci(self, name, slot, driver, config, legacy=False, options=""):
        self.c.execute('''
            INSERT INTO pci_slot(vmname, legacy, slot, driver, config, options)
            VALUES("%s", "%r", "%s", "%s", "%s", "%s")''' %
            (name, legacy, slot, driver, config, options))
        self.c.commit()

    def vm_list_pci(self, name):
        return self.c.execute(
            'SELECT * FROM pci_slot WHERE vmname = "%s" ORDER BY slot'%
            name).fetchall() 


if __name__ == "__main__":
    db = BeeDatabase()
    print db.vm_list()

