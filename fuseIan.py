#!/usr/bin/env python

from __future__ import with_statement, absolute_import

import os
import sys
import errno
import time
import stat

from fuse import FUSE, FuseOSError, Operations

# Using Fusypy RC April 5, 2018
class testOS(Operations):
    def __init__(self, root): # Need to add more parameters and more init values
        self.root = root
        self.files = {} # File stats for each virtual file
        self.fileName = 'testfile.txt'
        now = time.time()
        self.files['/'] = dict(st_mode=(stat.S_IFDIR | 0o777), st_ctime=now, st_mtime=now, st_atime=now, st_nlink=2)
        self.files['/geiger'] =  dict(st_mode=(stat.S_IFREG | 0o755), st_ctime=now, st_mtime=now, st_atime=now, st_nlink=2)
#        self.files['/geiger'] =  dict(st_mode=(stat.S_IFCHR | 0o755), st_ctime=now, st_mtime=now, st_atime=now, st_nlink=2)
        self.filehandle = {}

    def fullPath(self, partial):
        partial = partial.lstrip("/")
        path = os.path.join(self.root, partial)
        return path
        
    # getattr using Fusepy and the os module RC April 5, 2018
    def getattr(self, path, fh=None):
        print("getattr")
        full_path = self.fullPath(path)
        print(full_path)
        st = os.lstat(full_path)
        return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime', 'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))

    def access(self, path, mode):
        full_path = self.fullPath(path)
        if not os.access(full_path, mode):
            raise FuseOSError(errno.EACCES)

    def read(self, path, size, offset, fh):
        if (path == "/geiger"):
            return (os.read(self.filehandle, 5))        
        else:
            os.lseek(fh, offset, os.SEEK_SET)
            return os.read(fh, size)

    def write(self, path, buf, offset, fh):
        os.lseek(fh, offset, os.SEEK_SET)
        return os.write(fh, buf)

    def readdir(self, path, fh):
         print("readdir")
         full_path = self.fullPath(path)
         print(full_path)
         dirent = ['.', '..']
         if os.path.isdir(full_path):
              dirent.extend(os.listdir(full_path))
         for i in dirent:
             yield i
    
    def open(self, path, flags):
        if (path == "/geiger"):
            print("opengeiger")
            self.filehandle = os.open(self.fileName, flags)
        else:
            full_path = self.fullPath(path)
            return os.open(full_path, flags)

    def create(self, path, mode, fi=None):
        full_path = self.fullPath(path)
        return os.open(full_path, os.O_WRONLY | os.O_CREAT, mode)

    def flush(self, path, fh):
        return os.close(fh)

    def release(self, path, fh):
        return os.close(fh)

    def fsync(self, path, fdatasync, fh):
        return self.flush(path, fh)

if  __name__ == '__main__':
#    if len(argv != 1):
#        print('Not the correct arguments')
#        exit(1)			
    FUSE(testOS(sys.argv[1]), sys.argv[2], nothreads=True, foreground=True, ro=True)

