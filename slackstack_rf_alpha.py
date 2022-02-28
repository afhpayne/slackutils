#!/bin/env python3

# MIT License

# Copyright (c) 2019-2022 Andrew Payne

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

# build dictionary of local apps and libraries--------------------------------|
import glob
import os
from pathlib import Path
import shutil

# set home directory
home = str(Path.home())

installed_dict = {}


def build_dict_local_apps():
    for item in os.listdir("/var/log/packages/"):
        item = item.split(("-"))
        itembuild = item[-1].strip()
        if len(item[-1]) > 3:
            itemversion = item[-3]+" ("+itembuild+")"
            if len(item) == 7:
                itemname = item[0]+"-"+item[1]+"-"+item[2]+"-"+item[3]
                installed_dict.update({itemname:itemversion})
            elif len(item) == 6:
                itemname = item[0]+"-"+item[1]+"-"+item[2]
                installed_dict.update({itemname:itemversion})
            elif len(item) == 5:
                itemname = item[0]+"-"+item[1]
                installed_dict.update({itemname:itemversion})
            else:
                itemname = item[0]
                installed_dict.update({itemname:itemversion})
        # no tag means it's in the base system
        else:
            itemversion = item[-3]
            if len(item) == 7:
                itemname = item[0]+"-"+item[1]+"-"+item[2]+"-"+item[3]
                installed_dict.update({itemname:itemversion})
            elif len(item) == 6:
                itemname = item[0]+"-"+item[1]+"-"+item[2]
                installed_dict.update({itemname:itemversion})
            elif len(item) == 5:
                itemname = item[0]+"-"+item[1]
                installed_dict.update({itemname:itemversion})
            else:
                itemname = item[0]
                installed_dict.update({itemname:itemversion})    

    for item in os.listdir("/usr/bin/"):
        if not installed_dict.get(str(item)):
            installed_dict.update({item:"(version_unkown)"})    

    for item in os.listdir("/usr/lib64"):
        if item[0:3] == "lib":
            itemname = item[3:].split(".")
            itemname = itemname[0]
            if not installed_dict.get(str(itemname)):
                installed_dict.update({itemname:"(system library)"})
        else:
            if not installed_dict.get(str(itemname)):
                installed_dict.update({itemname:"(system library)"})
    return installed_dict

# build dictionary of remote apps and libraries-------------------------------|
sbo_categories = []
sbo_paths = {}
sbo_infofiles = []
sbo_app_list = []
sbo_ver_list = []
sbo_av_dict = {}


def build_dict_remote_apps():
    sbo_av_dict = {}
    for folder in glob.glob(home + "/slackware/dev_slack/"):
        if os.path.isdir(folder) and folder not in sbo_categories:
            sbo_categories.append(folder)
    
    for folder in glob.glob(home + "/slackware/dbs_slackware/"):
        if os.path.isdir(folder) and folder not in sbo_categories:
            sbo_categories.append(folder)
    
    for folder in glob.glob(home + "/slackstack/slackbuilds/*"):
        if os.path.isdir(folder) and folder not in sbo_categories:
            sbo_categories.append(folder)
    
    for folder in sbo_categories:
        for path in os.listdir(folder):
            if not sbo_paths.get(str(path)) \
               and os.path.isdir(folder+"/"+path) \
               and path != ".git":
                # print(folder+"/"+path)
                sbo_paths.update({path:folder})

    for path, folder in sbo_paths.items():
        with open(os.path.join(folder,path,path+".info"),"r") as f:
            lines = f.readlines()
            for line in lines:
                if "PRGNAM" in line:
                    prgnam = line.split('"')
                    sbo_app_list.append(prgnam[1])
                if "VERSION" in line:
                    version = line.split('"')
                    sbo_ver_list.append(version[1])

    sbo_av_dict = dict(zip(sbo_app_list, sbo_ver_list))
    return sbo_av_dict



def check_available_builds(app):
    for a,v in build_dict_remote_apps().items():
    # for a,v in sbo_av_dict.items():
        if a == app:
            print("Available version:",a,v)
            found = 1
            break
        else:
            found = 0
    if found == 0:
        print(app, "SlackBuild not found \n")
        exit()


def check_installed_builds(app):
    for a,v in build_dict_local_apps().items():
    # for a,v in installed_dict.items():
        if a == app:
            print("Installed version:",a,v,"\n")
            found = 1
            break
        else:
            found = 0
    if found == 0:
        print("Installed version:", "NONE", "\n")


def clean_tree():
    generic_path = (os.path.join(home,"slackstack"))
    kill_path = glob.glob(os.path.join(generic_path, "*-tree", ""))
    if kill_path:
        shutil.rmtree(os.path.join(kill_path[0]))


def copy_slackbuild_dirs_to_tree(app):
    remote_path = (os.path.join(sbo_paths[str(app)],app))
    local_path = (os.path.join(home,"slackstack",app_0+"-tree"+"/",app+"/"))
    print("Copying", app, "to", local_path)
    shutil.copytree(remote_path,local_path)


def check_for_dependencies():
    lines = []
    local_path = (os.path.join(home,"slackstack",app_0+"-tree"+"/"))
    for item in os.listdir(local_path):
        if item not in deps_checked_list:
            deps_checked_list.append(item)
            with open(local_path+item+"/"+item+".info", "r") as f:
                lines = f.readlines()
        else:
            continue
    for line in lines:
        if "REQUIRES" in line and len(line) > 12:
            line = line.replace("REQUIRES=","").replace('"','').strip()
            line = line.split(" ")
            for dep in line:
                deps_added_list.append(dep)
                if dep not in index_dict.values():
                    counter = (len(deps_added_list))
                    print(counter)
                    index_dict.update({counter:dep})
                    check_available_builds(dep)
                    check_installed_builds(dep)
                    copy_slackbuild_dirs_to_tree(dep)


# Let's get started
build_dict_remote_apps()
build_dict_local_apps()

print("What app are we building?")
app_0 = input("---> ")
print("")

x = 0
index_dict = {}

app = app_0
check_available_builds(app)
check_installed_builds(app)

clean_tree()

copy_slackbuild_dirs_to_tree(app)

print("\nDependencies:\n")
y = 1
deps_added_list = []
deps_checked_list = []
requires = []
for y in range (1, 10):
    check_for_dependencies()


exit(1)
