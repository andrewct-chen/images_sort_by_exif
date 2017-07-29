#!/usr/bin/python3.4
#
# gexiv2 image Exif date fixer.
# Corey Goldberg, 2014


"""Recursively scan a directory tree, fixing dates
on all jpg/png image files.
Each file's Exif metadata and atime/mtime are all
set to the file's ctime.
Modifications are done in-place.
Requires: gexiv2
"""

import sys
import os
import time

# GObject-based wrapper around the Exiv2 library.
# sudo apt-get install gir1.2-gexiv2-0.4
from gi.repository import GExiv2


def fix_image_dates(img_path):
    print (img_path)

    t = os.path.getctime(img_path)
    print ("file created time : ", t)
    ctime = time.strftime('%Y:%m:%d %H:%M:%S', time.localtime(t))
    print (ctime)

    t = os.path.getatime(img_path)
    print ("last accessed time : ", t)
    atime = time.strftime('%Y:%m:%d %H:%M:%S', time.localtime(t))
    print (atime)

    t = os.path.getatime(img_path)
    print ("last modified time : ", t)
    mtime = time.strftime('%Y:%m:%d %H:%M:%S', time.localtime(t))
    print (mtime)
    

    exif = GExiv2.Metadata(img_path)
    exif['Exif.Image.DateTime'] = ctime
    exif['Exif.Photo.DateTimeDigitized'] = ctime
    exif['Exif.Photo.DateTimeOriginal'] = ctime
    exif.save_file()
    os.utime(img_path, (t, t))

def print_file_path(major_path, minor_path, replaced_name):
    print (major_path)
    print (minor_path)
    print (replaced_name)

if __name__ == '__main__':
    argc_len = len(sys.argv)
    replaced_file_name = None
    if argc_len > 4 or argc_len < 3:
        print ("error argument counts")
        sys.exit()
    for i in range(argc_len):
        if i == 1:
            major_dir = sys.argv[i]
        if i == 2:
            minor_dir = sys.argv[i]
        if i == 3:
            replaced_file_name = sys.argv[i]
                

    print (" major_dir: ", major_dir)
    print (" minor_dir: ", minor_dir)
    print (" replaced_file_name: ", replaced_file_name)

    dir = '.'
    for root, dirs, file_names in os.walk(minor_dir):
        print ("minor root: ", root)
        print ("minor dirs: ", dirs)
        print ("minor file_names: ", file_names)
        for file_name in file_names:
            if file_name.lower().endswith(('jpg', 'png', 'jpeg')):
                img_path = os.path.join(root, file_name)
                for root, dirs, file_names in os.walk(major_dir):
                    print ("major root: ", root)
                    print ("major dirs: ", dirs)
                    print ("major file_names: ", file_names)
                    for file_name1 in file_names:
                        if file_name.lower().endswith(('jpg', 'png', 'jpeg')):
                            print_file_path(file_name1, file_name, None)
                
#                fix_image_dates(img_path)
