#!/bin/env python3

import glob
import hashlib
import os
import re
import readline
import shutil
import sys
import urllib.request

# Software Data:
soft_name = "Slackgrab"
soft_tag  = "a slackbuild tarball and binary downloader"

# Version
soft_vers = "0.5.6"

# Arguments
# --skip means don't ask about the download directory
try:
    arg_1 = sys.argv[1]
    print(arg_1)
except(IndexError):
    arg_1 = "0"
    pass

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

        prgnam = infofile.split()
        prgnam = prgnam[0].replace('PRGNAM="', "").strip('"')
        prgstem = prgnam[0:2].lower()

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
                with urllib.request.urlopen(url) as response, open(tarname, 'wb') as tarball:
                    shutil.copyfileobj(response, tarball)
                    
                hasher = hashlib.md5()
                with open(tarball.name, "rb") as tarball:
                    binary = tarball.read()
                    hasher.update(binary)
                print("\n" + "(" + prgnam + ") " + tarball.name + "\n")
                print("slackbuild md5sum  =", md5_list[c])
                print("actual file md5sum =", hasher.hexdigest())
                if md5_list[c] != hasher.hexdigest():
                    print("\n* * * CHECKSUMS DO NOT MATCH! * * *\n")
                else:
                    print("Checksum match :) \n")

                # Github has a naming problem, this fixes it
                if prgstem in tarball.name.strip().lower():
                    pass
                else:
                    tarball_name_fix = prgnam + "-" + tarball.name
                    os.rename((os.path.join(str(os.getcwd()) + "/" + str(tarname))), \
                              (os.path.join(str(os.getcwd()) + "/" + tarball_name_fix)))
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
            if a != 0:
                c = 0
                for url in url_list:
                    tarname = url.split('/')
                    tarname = tarname[-1]
                    tarname_text = str(tarname)
                    print("Downloading " + url)
                    with urllib.request.urlopen(url) as response, open(tarname, 'wb') as tarball:
                        shutil.copyfileobj(response, tarball)

                    hasher = hashlib.md5()
                    with open(tarball.name, "rb") as tarball:
                        binary = tarball.read()
                        hasher.update(binary)
                    print("\n" + "(" + prgnam + ") " + tarball.name + "\n")
                    print("slackbuild md5sum  =", md5_list[c])
                    print("actual file md5sum =", hasher.hexdigest())
                    if md5_list[c] != hasher.hexdigest():
                        print("\n* * * CHECKSUMS DO NOT MATCH! * * *\n")
                    else:
                        print("Checksum match :) \n")

                    # # Github has a naming problem, this fixes it
                    if prgstem in tarball.name.strip().lower():
                        pass
                    else:
                        tarball_name_fix = prgnam + "-" + tarball.name
                        os.rename((os.path.join(str(os.getcwd()) + "/" + str(tarname))), \
                                  (os.path.join(str(os.getcwd()) + "/" + tarball_name_fix)))
                    c += 1


if arg_1 == "--skip" or arg_1 == "-s":
    for dir in os.scandir(os.path.join(build_path)):
        currentwd = dir
        # print(currentwd)
        tar_grab_func()
else:
    print("\nIterate all folders in [", build_path, "] ?")
    yes_or_no = input("y/n: ")
    if yes_or_no == "Y" or yes_or_no == "y":
        for dir in os.scandir(os.path.join(build_path)):
            currentwd = dir
            # print(currentwd)
            tar_grab_func()
    else: 
        print("\nOk, use current: [", os.getcwd(), "] ?")
        yes_or_no = input("y/n: ")
        if yes_or_no == "N" or yes_or_no == "n":
            print("")
            exit(0)
        else:
            print("Using current directory")
            tar_grab_func()
