from __future__ import with_statement, absolute_import

import os
import sys
import errno
import time
import stat

from fuse import FUSE, FuseOSError, Operations

# Using Fusypy RC April 5, 2018
class testOS(Operations):
    def __init__(self): # Need to add more parameters and more init values
        self.files = {} # File stats for each virtual file
        self.fileName = 'testfile.txt'
        now = time.time()
        self.files['/'] = dict(st_mode=(stat.S_IFDIR | 0o777), st_ctime=now, st_mtime=now, st_atime=now, st_nlink=2)
        self.files['/geiger'] =  dict(st_mode=(stat.S_IFREG | 0o755), st_ctime=now, st_mtime=now, st_atime=now, st_nlink=2)
#        self.files['/geiger'] =  dict(st_mode=(stat.S_IFCHR | 0o755), st_ctime=now, st_mtime=now, st_atime=now, st_nlink=2)
        self.filehandle = {}
        
    # getattr using Fusepy and the os module RC April 5, 2018
    def getattr(self, path, fh=None):
        print("getattr")
        print(self.files)
        print(path)
        if path not in self.files:    # Path is not in file
            raise FuseOSError(errno.ENOENT) # Error No Entity

        self.files[path]['st_ctime'] = os.stat(self.fileName).st_ctime
        # Time of last file status change
 
        self.files[path]['st_mtime'] = os.stat(self.fileName).st_mtime
        # Time of last data modification

        self.files[path]['st_atime'] = os.stat(self.fileName).st_atime
        # Time of most recent access

        self.files[path]['st_size'] = os.stat(self.fileName).st_size
        # Size of file, in bytes
        return self.files[path]
    
    def read(self, path, size, offset, fh):
        if (path == "/geiger"):
            return (os.read(self.filehandle, 5))        
        else:
            print("readelse")
        return 0

    def readdir(self, path, fh):
         print("readdir")
         print(path)
         for direct in '.','..', 'geiger':
             yield direct
            

    
    def open(self, path, flags):
        if (path == "/geiger"):
            print("opengeiger")
            self.filehandle = os.open(self.fileName, flags)
        else:
            print("openelse")
        return 0

    

FUSE(testOS(), sys.argv[1], nothreads=True, foreground=True, ro=True)
