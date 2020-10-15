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
soft_vers = "0.5.7"

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

infolist = []
download_list = []
md5_list = []
download_64_list = []
md5_64_list = []

def slackgrab_func():
    infofile = glob.glob(os.path.join(currentwd, "*.info"))
    if infofile:
        # os.chdir(currentwd)
        with open(infofile[0]) as i:
            infofile = i.read()    
        for row in infofile.split("\n"):
            row=row.strip()
            infolist.append(row)


    def parse_info_func(infofile, first, last):
        start = infofile.index(first) + len(first)
        end = infofile.index(last, start)
        return infofile[start:end]


    download = (parse_info_func(infofile, "DOWNLOAD=", "MD5SUM="))
    if download:
        download = download.replace('"', '').replace("\\", "")
    for item in download.split():
        if "UNSUPPORTED" not in item:
            download_list.append(item)

    md5 = (parse_info_func(infofile, "MD5SUM=", "DOWNLOAD_x86_64="))
    if md5:
        md5 = md5.replace('"', '').replace("\\", "")
    for item in md5.split():
        md5_list.append(item)      

    download_64 = (parse_info_func(infofile, "DOWNLOAD_x86_64=", "MD5SUM_x86_64="))
    if download_64:
        download_64 = download_64.replace('"', '').replace("\\", "")
    for item in download_64.split():
        download_64_list.append(item)

    md5_64 = (parse_info_func(infofile, "MD5SUM_x86_64=", "REQUIRES="))
    if md5_64:
        md5_64 = md5_64.replace('"', '').replace("\\", "")
    for item in md5_64.split():
        md5_64_list.append(item)
    
    print(download_64_list)
    # if there are 32 bit tars we choose 64
    if "http" in str(download_64_list):
        url_list = download_64_list
        hash_list = md5_64_list
    else:
        url_list = download_list
        hash_list = md5_list


    def get_tar_func():
        for url in url_list:
            tarname = url.split('/')
            tarname = tarname[-1]
            print("Downloading " + url)
            with urllib.request.urlopen(url) as response, open(tarname, 'wb') as tarname:
                print(response)
                exit()
                shutil.copyfileobj(response, tarname)


    def check_md5_func():
        c = 0
        for url in download_list:
            tarname = url.split('/')
            tarname = tarname[-1]
            hasher = hashlib.md5()
            with open(tarname, "rb") as tarname:
                binary = tarname.read()
                hasher.update(binary)
            print("\n" + tarname.name + "\n")
            print("slackbuild md5sum  =", hash_list[c])
            print("actual file md5sum =", hasher.hexdigest())
            if md5_list[c] != hasher.hexdigest():
                print("\n* * * CHECKSUMS DO NOT MATCH! * * *\n")
            else:
                print("Checksum match :) \n")
            c += 1
    get_tar_func()
    check_md5_func()

# slackgrab_func()

if arg_1 == "--skip" or arg_1 == "-s":
    for directory in os.scandir(os.path.join(build_path)):
        if os.path.isdir(directory):
            currentwd = directory
            print(directory)
            slackgrab_func()
else:
    print("\nIterate all folders in [", build_path, "] ?")
    yes_or_no = input("y/n: ")
    if yes_or_no == "Y" or yes_or_no == "y":
        for dir in os.scandir(os.path.join(build_path)):
            currentwd = dir
            # print(currentwd)
            slackgrab_func()
    else: 
        print("\nOk, use current: [", os.getcwd(), "] ?")
        yes_or_no = input("y/n: ")
        if yes_or_no == "N" or yes_or_no == "n":
            print("")
            exit(0)
        else:
            print("Using current directory")
            slackgrab_func()




        #             # # Github has a naming problem, this fixes it
        #             if prgstem in tarball.name.strip().lower():
        #                 pass
        #             else:
        #                 tarball_name_fix = prgnam + "-" + tarball.name
        #                 os.rename((os.path.join(str(os.getcwd()) + "/" + str(tarname))), \
        #                           (os.path.join(str(os.getcwd()) + "/" + tarball_name_fix)))
        #             c += 1
