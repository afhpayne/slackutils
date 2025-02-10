#!/bin/env python3

# MIT License

# Copyright (c) 2019-2025 Andrew Payne

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# 79 spaces-------------------------------------------------------------------|

import glob
import os
import platform
import re
import shutil
import stat
import subprocess
import sys
import time

# Software Data:
soft_name = "Slackstack"
soft_tag  = "a slackbuild utility"

# Version
soft_vers = "0.23.2"

with open(os.path.join("/etc/os-release"), 'r') as file:
    for line in file:
        if "current" in line:
            relname = "current"
        else:
            relname = "stable"

# set home directory
path = "~"
home = os.path.expanduser(path)
dir_sst = os.path.join(home, "slackstack")
dir_fork = os.path.join(home, dir_sst, "slackbuilds")
dir_sbo = os.path.join(home, "slackware/sbo_slack")
dir_dbs = os.path.join(home, "slackware/dbs_slack")
dir_dev = os.path.join(home, "slackware/dev_slack")

# skip dir_dev if we're not using current
if relname == "stable":
    dir_dev = dir_dbs

# # This is the git repo to use for sbo
sbo_git = "https://gitlab.com/SlackBuilds.org/slackbuilds.git"

pack_full_name = []
pack_clean_name = []
system_dict = {}
sbo_dict = {}
dep_list = []
install_order_list = []
install_dict = {}
version_dict = {}
ver_list = []

subprocess.run(["mkdir", "-p", dir_fork])

os.system("clear")
welstr = ("Welcome to " \
          + soft_name \
          + " version "
          + soft_vers + ", " \
          + soft_tag + "." \
          + "\n\nSystem is: " + "Slackware " + relname)
print("\n" + welstr)
print("")

# update git
print("Updating git")
if os.path.isdir(dir_fork + "/" + ".git"):
    subprocess.run(["git", "-C", dir_fork, "pull"])
else:
    subprocess.run(["git", "clone", sbo_git, dir_fork])
time.sleep(1)

# remove existing tree directory
kill_path = glob.glob(os.path.join(dir_sst, "*-tree", ""))
if kill_path:
    shutil.rmtree(os.path.join(kill_path[0]))

# create list of local installs
for i in os.scandir("/var/log/packages"):
    pack_full_name.append(i.name)

# clean off architecture
for full in pack_full_name:
    strip = re.findall(r"(-x86.*|-noarch.*)", full)
    if strip:
        full = full.replace(strip[0], "")
        full = full.split("-")
        pack_clean_name.append(full)

# build dict of local packages and versions        
pack_full_name = []
pack_clean_name.sort()
for clean in pack_clean_name:
    app = ""
    ver = clean[-1]
    clean.pop()
    while len(clean) > 0:
        app = app + clean[0] + "-"
        clean.pop(0)
    system_dict.update({app[:-1]:ver})

# add python modules to list of local packages
py_list = []
subprocess.run(["pip list > /tmp/pip.txt"], shell=True,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.STDOUT)
with open(os.path.join("/tmp/pip.txt"), 'r') as file:
    for line in file:
        line_alt1 = line.replace ("_", "-")
        line_alt2 = line.replace ("-", "_")
        line = "python3-" + line
        line_alt1 = "python3-" + line_alt1
        line_alt2 = "python3-" + line_alt2
        py_list.append(line.strip().split())
        py_list.append(line_alt1.strip().split())
        py_list.append(line_alt2.strip().split())
for module in py_list:
    system_dict.update({module[0] : module[1]})

# create dict of sbo programs
for i in os.walk(dir_fork):
    sublist = (i[0].split("/"))
    if len(sublist) == 7 and ".git" not in sublist:
        sbo_dict.update({sublist[-1]:i[0]})

# update sbo programs dict with personal builds
for i in os.walk(dir_sbo):
    sublist = (i[0].split("/"))
    if len(sublist) == 6 and ".git" not in sublist:
        sbo_dict.update({sublist[-1]:i[0]})

# update sbo programs dict with personal builds
for i in os.walk(dir_dbs):
    sublist = (i[0].split("/"))
    if len(sublist) == 6 and ".git" not in sublist:
        sbo_dict.update({sublist[-1]:i[0]})

# update sbo programs dict with dev builds for -current
# nullified if slack version is not current
# for i in os.walk(dir_dev):
#     sublist = (i[0].split("/"))
#     if len(sublist) == 6 and ".git" not in sublist:
#         sbo_dict.update({sublist[-1]:i[0]})

for i in os.walk(dir_dev):
    if os.path.isdir(i[0]) and ".git" not in i[0]:
        sublist = (i[0].split("/"))
        if len(sublist) == 6 and "tree" not in sublist[-1]:
            sbo_dict.update({sublist[-1]:i[0]})
        elif len(sublist) == 7 and "tree" in sublist[-2]:
            sbo_dict.update({sublist[-1]:i[0]})
        
# os.system("clear")
# welstr = ("Welcome to " \
#           + soft_name \
#           + " version "
#           + soft_vers + ", " \
#           + soft_tag + "." \
#           + "\n\nSystem is: " + relname[0])
# print("\n" + welstr)
# print("")

userapp = input("\nWhat app are we building? ")
# userapp = [userapp]

# build dict of install candidate
for app,path in sbo_dict.items():
    if userapp == app:
        with open(os.path.join(path, app + ".info")) as info:
            lines = info.readlines()
            ver = lines[1]
            install_dict.update({app:ver[9:-2]})
            version_dict.update({app:ver[9:-2]})            
            dep_list.append(app)
            
# fail if no app
if dep_list:
    local_path = (os.path.join(dir_sst, userapp + "-tree" + "/"))
    subprocess.run(['mkdir', '-p', local_path])
    pass
else:
    print("\n" + userapp, "not found\n")
    exit(1)
    
# build dict of dependencies
x = 0
y = 101
while x < 100:
    for dep in dep_list:
        for app, path in sbo_dict.items():
            if app == dep:
                with open(os.path.join(path, app + ".info")) as info:
                    lines = info.readlines()
                    dep = lines[-3]
                    dep = dep[10:-2].split(" ")
                    for d in dep:
                        if d != "" and d not in dep_list:
                            dep_list.append(d)
                            install_dict.update({d:y})
                            version_dict.update({d:y})            
                            y += 1
                    # dep_list.pop(0)
            x += 1

# create printable ordered list of dependencies
for a,b in install_dict.items():
    if a != userapp:
        install_order_list.append([str(b), a])
install_order_list.append([str(100), userapp])
install_order_list.sort()
install_order_list.reverse()

# add versions to version dict
for app,num in version_dict.items():
    for sbo_app,sbo_path in sbo_dict.items():
        if app == sbo_app:
            with open(os.path.join(sbo_path, sbo_app + ".info")) as info:
                lines = info.readlines()
                ver = lines[1]
                version_dict.update({app:ver[9:-2]})

for a,b in install_dict.items():
    for sbo_app,sbo_path in sbo_dict.items():
        if a == sbo_app:
            with open(os.path.join(sbo_path, sbo_app + ".info")) as info:
                lines = info.readlines()
                ver = lines[1]
                ver_list.append("\nAVAILABLE\t" + sbo_app + " " + ver[9:-2])
    for sys_app,sys_ver in system_dict.items():
        if a == sys_app:
            ver_list.append("INSTALLED\t" + sys_app + " " + sys_ver)
        elif a not in system_dict:
            ver_list.append("INSTALLED\t" + a + " is not installed")
            break

for item in ver_list:
    print(item)
print("")

for app,num in install_dict.items():
    for sbo_app,sbo_path in sbo_dict.items():
        if app == sbo_app:
            subprocess.run(['rsync', '-a', sbo_path, local_path])

# write text file with install order
lenlist = []
x = 100
io_path = os.path.join(dir_sst, userapp + "-tree")
with open(os.path.join(io_path, "install_order_list.txt"), "w") as f:
    for item in install_order_list:
        lenlist.append(item[1])
        n = max(lenlist, key=len)
    for item in install_order_list:
        textline = x
        textline = (str(textline) + " "*3 + item[1] + (" " * ((len(n)+3) - len(item[1]))))
        for app,ver in system_dict.items():
            if item[1] == app:
                textline = (textline + "(installed version)" + "\t" + ver)
        x += 1
        f.write(textline + "\n")

# run or not slackgrab to get tarballs
grab_y_n = input("Run slackgrab.py to get the tarballs (y/n)? ")
if grab_y_n == "Y" or grab_y_n == "y":
    subprocess.run(["slackgrab.py", "--skip"], cwd=sys.path[0])
else:
    pass

for item in glob.glob(local_path + "/*/*"):
    if "SlackBuild" in item:
        perms = os.stat(item)
        os.chmod(item, perms.st_mode | stat.S_IEXEC)

exit()
