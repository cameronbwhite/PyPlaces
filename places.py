#!/usr/bin/env python
# places.database.py
import sqlite3
import IPython
import os

class Places(object):
    def __init__(self, path):
        """ """
        path = IPython.utils.path.expand_path(path)
        self.connection = sqlite3.connect(path)  
        self.cursor = self.connection.cursor()
        self._createTables()
    def close(self):
        """ """
        self.connection.close()
    def add(self, place_name, user_name, host, ssh_port):
        """ """
        self.cursor.execute('''
            INSERT INTO places (
                    place_name,
                    user_name, 
                    host, 
                    ssh_port 
                ) VALUES (?,?,?,?)
        ''', (place_name, user_name, host, ssh_port))
        self.connection.commit()
    def list(self):
        """ """
        self.cursor.execute('''
            SELECT 
                place_name, user_name, host, ssh_port 
            FROM places
        ''')
        return self.cursor.fetchall()
    def connect(self, place_name):
        self.cursor.execute('''
            SELECT user_name, host, ssh_port 
            FROM places
            WHERE place_name=?
        ''', (place_name,))
        place = self.cursor.fetchone()
        command = 'ssh {}@{} -p {}'.format(place[0],place[1],place[2])
        os.system(command)
    def _createTables(self):
        """ """
        try:
            self.cursor.execute('''
                CREATE TABLE places (
                    place_name TEXT PRIMARY KEY,
                    user_name TEXT,
                    host TEXT,
                    ssh_port INTEGER
                )
            ''')
        except sqlite3.OperationalError as exception:
            print('ERROR')
