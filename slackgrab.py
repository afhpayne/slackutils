#!/bin/env python3

# Software Data:
soft_name = "Slackgrab"
soft_tag  = "a slackbuild tarball and binary downloader"

# Version
soft_vers = "0.5.1"

import urllib.request
import shutil
import os
import glob
import hashlib
import re
import readline

os.system("clear")
welstr = ("Welcome to " + soft_name + " version " + soft_vers + ", " + soft_tag + ".")
print("\n" + welstr)

currentwd   = os.getcwd()
build_home  = os.path.join(os.environ['HOME'], "slackstack", "")
build_prog  = glob.glob(build_home + "*-tree")
build_path  = os.path.join(str(build_prog))
build_path  = build_path.strip("[").strip("]").strip("'")

def tar_grab_func():
    infofile = glob.glob(os.path.join(currentwd, "*.info"))
    if infofile:
        infofile = infofile[0]
        os.chdir(currentwd)

        with open(infofile) as i:
            infofile = i.read()
        i.closed
        
        line_list   = []
        check_64bit = []
        url_list    = []
        md5_list    = []
        a = 0
        b = 0
        
        back_half_url = infofile.split("DOWNLOAD_x86_64=")
        for item in back_half_url[1].split():
            if "http" in item:
                url_list.append(item.strip('"'))
                a += 1
        back_half_md5 = infofile.split("MD5SUM_x86_64=")
        for item in back_half_md5[1].split():
            if len(item) > 5 and b < a:
                md5_list.append(item.strip('"'))
                b += 1
        if a != 0:
            c = 0
            for url in url_list:
                tarname = url.split('/')
                tarname = tarname[-1]
                tarname_text = tarname
                print("Downloading " + url)
                with urllib.request.urlopen(url) as response, open(tarname, 'wb') as tarname:
                    shutil.copyfileobj(response, tarname)
                    
                hasher = hashlib.md5()
                with open(tarname_text, "rb") as tarball:
                    binary = tarball.read()
                    hasher.update(binary)
                print("\n" + tarname_text + "\n")
                print("slackbuild md5sum  =", md5_list[c])
                print("actual file md5sum =", hasher.hexdigest())
                if md5_list[c] != hasher.hexdigest():
                    print("\n* * * CHECKSUMS DO NOT MATCH! * * *\n")
                else:
                    print("Checksum match :) \n")
                c += 1
        else:
            front_half_url = infofile.split("DOWNLOAD=")
            for item in front_half_url[1].split():
                if "http" in item:
                    url_list.append(item.strip('"'))
                    a += 1
            front_half_md5 = infofile.split("MD5SUM=")
            for item in front_half_md5[1].split():
                if len(item) > 5 and b < a:
                    md5_list.append(item.strip('"'))
                    b += 1
            c = 0
            for url in url_list:
                tarname = url.split('/')
                tarname = tarname[-1]
                tarname_text = tarname
                print("Downloading " + url)
                with urllib.request.urlopen(url) as response, open(tarname, 'wb') as tarname:
                    shutil.copyfileobj(response, tarname)
                    
                hasher = hashlib.md5()
                with open(tarname_text, "rb") as tarball:
                    binary = tarball.read()
                    hasher.update(binary)
                print("\n" + tarname_text + "\n")
                print("slackbuild md5sum  =", md5_list[c])
                print("actual file md5sum =", hasher.hexdigest())
                if md5_list[c] != hasher.hexdigest():
                    print("\n* * * CHECKSUMS DO NOT MATCH! * * *\n")
                else:
                    print("Checksum match :) \n")
                c += 1

print("\nIterate all folders in [", build_path, "] ?")
yes_or_no = input("y/n: ")
if yes_or_no == "N" or yes_or_no == "n":
    print("\nOk, use current: [", os.getcwd(), "] ?")
    yes_or_no = input("y/n: ")
    if yes_or_no == "N" or yes_or_no == "n":
        exit(0)
    else:
        print("Using current directory")
        tar_grab_func()
else:
    for dir in os.scandir(os.path.join(build_path)):
        currentwd = dir
        print(currentwd)
        tar_grab_func()
