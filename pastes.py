#!/usr/bin/env python
# encoding: utf-8

#Pasteros Paste at pasteros.io

# Copyright (C) 2015
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Detect if data was piped in or not
# http://stackoverflow.com/questions/13442574/how-do-i-determine-if-sys-stdin-is-redirected-from-a-file-vs-piped-from-another

"""This is a script to use the Pasteros.io api"""

import urllib2
import sys
import stat
import os
import fileinput
import sqlite3
import json
import argparse

def tell_flake_to_shutup():
    sqlite3
    sys
    urllib2

class Upload:
    def __init__(self, name = None, content = None, language = None, tag = None,
        visibility = "false", file_ = None):

        # JSON Values
        self.name       = name
        self.content    = content
        self.language   = language
        self.tag        = tag
        self.visibility = visibility
        self.file_      = file_

        # API Values
        self.site       = "https://pasteros.io/"
        self.api        = "api/v1/create"
        self.uri        = self.site + self.api
        self.data       = None
        self.id_        = None
        self.delete     = None
        self.response   = None

        # Check to see if we're uploading a file
        # And then read it.
        if self.file_:
            #print "file exits!!!!"
            self.create_content()

    def create_content(self):
        print "Creating Content from file"
        with open(self.file_) as f:
            file_contents = "".join(f.readlines())
            #print "".join(file_contents)
            #print file_contents
            self.content = file_contents

    def create_json(self):
        self.data = json.dumps({
            'name'      : self.name,
            'content'   : self.content,
            'language'  : self.language,
            'visibility': self.visibility,
            'tag'       : self.tag,
            })
        return self.data

    def get_json(self):
        """This is where we want to deal with handling responses"""
        pass
                
    
    def upload(self):
        # Gotta pass in self.data to the API values
        r = urllib2.Request(url=self.uri, data=self.data)
        r = urllib2.urlopen(r)
        r =  r.read()
        #print r
        self.response = json.loads(r)

    def read_response(self):
        # Test response
        #self.response = { 'id' : 25235, 'delete_id' : 1235235}
        print self.site + str(self.response['id'])
        print (self.site + str(self.response['id']) +
        "/delete/" + str(self.response['delete_id']))

    def __str__(self):
        tmpls = []
        for e, item in enumerate([self.name, self.content, self.language,
            self.tag, self.visibility]):
            if not item:
                tmpls.append("none")
            else:
                tmpls.append(item)
        return " ".join(tmpls)

def parse_flag():

    languages = [
            'bash', 'c++', 'c#', 'css', 'diff', 'java', 'javascript', 'perl',
            'php', 'plain', 'python', 'ruby', 'sql', 'xml',
            ]

    # Requires a file to upload
    parser = argparse.ArgumentParser()
    parser.add_argument('file', nargs='+',  help="Put either a file, or raw"
    "text")
    parser.add_argument('-n', '--name',     help="Name of the paste")
    parser.add_argument('-t', '--tag',      help="Tag description of paste")
    parser.add_argument('-l', '--language', help="Programming language",
            choices=languages)
    #parser.add_argument('-c', '--content',  help="What you are pasting")
    args = parser.parse_args()

    content =  " ".join(args.file)
    content_or_file = None
    if os.path.exists(content):
        # This is where we setup the dictionary values
        content_or_file = 'file_'
    else:
        content_or_file = 'content'

    return {'name' : args.name, 'tag' : args.tag, 'language' : args.language,
            content_or_file: content}

if __name__ == '__main__':
    print "running..."
    mode = os.fstat(0).st_mode

    # This is to check if data is being piped in,
    # we'll add this later
    if stat.S_ISFIFO(mode):
        #text = sys.stdin.read()
        txt = []
        for line in fileinput.input():
            txt.append(line.strip(''))
        print " ".join(txt)
        #print fileinput.filename()

        text = " ".join(txt)
        
        #upload(text)
    else:
        # Data is NOT being piped in, normal cli tools
        # Cool **parse_flag works with unpacking
        u = Upload(**parse_flag())
        u.create_json()
        u.upload()
        u.read_response()