#!/bin/env python3

# MIT License

# Copyright (c) 2019-2024 Andrew Payne

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
soft_vers = "0.2.0"

# set home directory
path = "~"
home = os.path.expanduser(path)
dir_sst = os.path.join(home, "slackstack")
dir_sbo = os.path.join(home, dir_sst, "slackbuilds")
dir_dbs = os.path.join(home, "slackware/dev_slack")

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

os.system("clear")
welstr = ("Welcome to " \
          + soft_name \
          + " version "
          + soft_vers + ", " \
          + soft_tag + ".")
print("\n" + welstr)
print("")

subprocess.run(["mkdir", "-p", dir_sbo])

# update git
print("Updating git")
if os.path.isdir(dir_sbo + "/" + ".git"):
    subprocess.run(["git", "-C", dir_sbo, "pull"])
else:
    subprocess.run(["git", "clone", sbo_git, dir_sbo])
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

# create dict of sbo programs
for i in os.walk(dir_sbo):
    sublist = (i[0].split("/"))
    if len(sublist) == 7 and ".git" not in sublist:
        sbo_dict.update({sublist[-1]:i[0]})

# update sbo programs dict with personal builds
for i in os.walk(dir_dbs):
    sublist = (i[0].split("/"))
    if len(sublist) == 6 and ".git" not in sublist:
        sbo_dict.update({sublist[-1]:i[0]})


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
            if dep == app:
                with open(os.path.join(path, app + ".info")) as info:
                    lines = info.readlines()
                    dep = lines[-3]
                    dep = dep[10:-2].split(" ")
                    for d in dep:
                        if d != "":
                            dep_list.append(d)
                            install_dict.update({d:y})
                            version_dict.update({d:y})            
                            y += 1
                    dep_list.pop(0)
    x += 1

# create printable ordered list of dependencies
for a,b in install_dict.items():
    if a != userapp:
        install_order_list.insert(0, str(b) + " " + a)
install_order_list.sort()
install_order_list.reverse()
install_order_list.append(str(100) + " " + userapp)

y = len(install_order_list)
for install in install_order_list:
    install = install[3:]
    install = str(y) + install
    y-=1

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

for item in glob.glob(local_path + userapp + "/*"):
    if "SlackBuild" in item:
        perms = os.stat(item)
        os.chmod(item, perms.st_mode | stat.S_IEXEC)

# write text file with install order
io_path = os.path.join(dir_sst, userapp + "-tree")
with open(os.path.join(io_path, "install_order_list.txt"), "w") as f:
    f.write("install_order_list:\n")
    for app in install_order_list:
        f.write(app + "\n")

# run or not slackgrab to get tarballs
grab_y_n = input("Run slackgrab.py to get the tarballs (y/n)? ")
if grab_y_n == "Y" or grab_y_n == "y":
    subprocess.run(["slackgrab.py", "--skip"], cwd=sys.path[0])
else:
    pass

exit()
