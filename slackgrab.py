#!/bin/env python3

# MIT License

# Copyright (c) 2019-2022 Andrew Payne

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# 79 spaces-------------------------------------------------------------------|

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
soft_vers = "0.6.1"

build_home = os.path.join(os.environ['HOME'], "slackstack", "")
build_path = glob.glob(build_home + "*-tree")
build_path = build_path[0].strip()

infolist = []
download_list = []
md5_list = []
download_64_list = []
md5_64_list = []
bad_list = []

def hello_string():
    os.system("clear")
    hellostr = ("Welcome to " + soft_name + " version "
              + soft_vers + ", " + soft_tag + ".")
    print("\n" + hellostr)
    print("")


def slackgrab_func():
    infofile = glob.glob(os.path.join(currentwd, "*.info"))
    os.chdir(currentwd)
    with open(infofile[0]) as i:
        infofile = i.read()
        i.closed
    for row in infofile.split("\n"):
        row = row.strip()
        infolist.append(row)


    def parse_info_func(infofile, first, last):
        start = infofile.index(first) + len(first)
        end = infofile.index(last, start)
        return infofile[start:end]


    download = parse_info_func(infofile, "DOWNLOAD=", "MD5SUM=")
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

    download_64 = (parse_info_func(
        infofile, "DOWNLOAD_x86_64=", "MD5SUM_x86_64="))
    if download_64:
        download_64 = download_64.replace('"', '').replace("\\", "")
    for item in download_64.split():
        download_64_list.append(item)

    md5_64 = (parse_info_func(
        infofile, "MD5SUM_x86_64=", "REQUIRES="))
    if md5_64:
        md5_64 = md5_64.replace('"', '').replace("\\", "")
    for item in md5_64.split():
        md5_64_list.append(item)
    
    # if there are 32 bit tars we choose 64
    if "http" in str(download_64_list):
        url_list = download_64_list
        hash_list = md5_64_list
    else:
        url_list = download_list
        hash_list = md5_list


    def get_tar_func():
        for url in url_list:
            req = urllib.request.Request(
                url, headers={"User-Agent": "Chrome"})
            tarname = url.split('/')
            tarname = tarname[-1]
            print("Downloading " + url)
            with urllib.request.urlopen(req) as response, open(
                    tarname, 'wb') as tarname:
                shutil.copyfileobj(response, tarname)


    def check_md5_func():
        counter = 0
        for url in url_list:
            tarname = url.split('/')
            tarname = tarname[-1]
            hasher = hashlib.md5()
            with open(tarname, "rb") as tarname:
                binary = tarname.read()
                hasher.update(binary)
            print("\n" + tarname.name + "\n")
            print("slackbuild md5sum  =", hash_list[counter])
            print("actual file md5sum =", hasher.hexdigest())
            if hash_list[counter] != hasher.hexdigest():
                print("\n* * * CHECKSUMS DO NOT MATCH! * * *\n")
                bad_list.append(tarname.name)
            else:
                print("Checksum match :) \n")
            counter += 1


    get_tar_func()
    check_md5_func()


# Let's get started
hello_string()

# Arguments
# --skip means don't ask about the download directory
try:
    arg_1 = sys.argv[1]
    print(arg_1)
except(IndexError):
    arg_1 = "0"
    pass

if arg_1 == "--skip" or arg_1 == "-s":
    for path in next(os.walk(build_path))[1]:
        currentwd = os.path.join(build_path, path, "")
        print("\nScanning", currentwd, "\n")
        slackgrab_func()
        download_list = []
        md5_list = []
        download_64_list = []
        md5_64_list = []

else:
    print("\nIterate all folders in [", build_path, "] ?")
    yes_or_no = input("y/n: ")
    if yes_or_no == "Y" or yes_or_no == "y":
        for path in next(os.walk(build_path))[1]:
            currentwd = os.path.join(build_path, path, "")
            print("\nScanning", currentwd, "\n")
            slackgrab_func()
            download_list = []
            md5_list = []
            download_64_list = []
            md5_64_list = []
    else: 
        print("\nOk, use current: [", os.getcwd(), "] ?")
        yes_or_no = input("y/n: ")
        if yes_or_no == "N" or yes_or_no == "n":
            print("")
            exit(0)
        else:
            build_path = os.getcwd()
            print("Using current directory")
            for path in next(os.walk(build_path))[1]:
                currentwd = os.path.join(build_path, path, "")
                print("\nScanning", currentwd, "\n")
                slackgrab_func()
                download_list = []
                md5_list = []
                download_64_list = []
                md5_64_list = []

if len(bad_list) > 0:
    for item in bad_list:
        print("The MD5SUM for", item, "did not check out.")
    print("")
    exit()
else:
    exit()
