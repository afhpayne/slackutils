#!/bin/env python3

# Version = 0.4.1

import urllib.request
import shutil
import os
import glob
import hashlib

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

        global tarname
        global true_md5

        for line in infofile.split("\n"):
            if "DOWNLOAD_x86_64=" in line:
                url_64b = line.strip()
                url_64b = url_64b.split('"')[1]
                if url_64b != '':
                    print("\nURL =", url_64b)
                    tar_64b = url_64b.split("/")
                    tar_64b = (tar_64b[-1])
                    print("\nFile name =", tar_64b)
                    tarname = tar_64b
                    if tar_64b != '':
                        with urllib.request.urlopen(url_64b) as response, open(tar_64b, 'wb') as tar_64b:
                            shutil.copyfileobj(response, tar_64b)
                else:
                    for line in infofile.split("\n"):
                        if "DOWNLOAD=" in line:
                            url_32b = line.strip()
                            url_32b = url_32b.split('"')[1]
                            if url_32b != '':
                                print("\nURL = ", url_32b)
                                tar_32b = url_32b.split("/")
                                tar_32b = (tar_32b[-1])
                                print("\nFile name =", tar_32b)
                                tarname = tar_32b
                                if tar_32b != '':
                                    with urllib.request.urlopen(url_32b) as response, open(tar_32b, 'wb') as tar_32b:
                                        shutil.copyfileobj(response, tar_32b)

        for line in infofile.split("\n"):
            if "REQUIRES=" in line:
                depends = line.strip()
                depends = depends.split('"')[1]
                print("\nThis software requires:")
                for dep in depends.split(" "):
                    print("-->", dep)

        for line in infofile.split("\n"):
            if "MD5SUM_x86_64=" in line:
                true_md5 = line.strip()
                true_md5 = true_md5.split('"')[1]
                if true_md5 != '':
                    continue
                else:
                    for line in infofile.split("\n"):
                        if "MD5SUM=" in line:
                            true_md5 = line.strip()
                            true_md5 = true_md5.split('"')[1]
        
        print("")
        print(true_md5, "= Slackbuild MD5")
        
        def md5(tarname):
            m = hashlib.md5()
            with open(tarname, "rb") as f:
                for block in iter(lambda: f.read(), b""):
                    m.update(block)
                    return m.hexdigest()
        
        print(md5(tarname), "=", tarname)
        
        if md5(tarname) == true_md5:
            print("The checksums match!\n")
        else:
            print("WARNING: checksum mismatch!\n")

print("\nIterate all folders in [", build_path, "] ?")
yes_or_no = input("y/n: ")
if yes_or_no == "N" or yes_or_no == "n":
    print("\nOk, use current: [", os.getcwd(), "] ?")
    yes_or_no = input("y/n: ")
    if yes_or_no == "N" or yes_or_no == "n":
        exit(0)
    else:
        print("TAR GRAB SOLO")
        tar_grab_func()
else:
    for dir in os.scandir(os.path.join(build_path)):
        currentwd = dir
        print(currentwd)
        tar_grab_func()
