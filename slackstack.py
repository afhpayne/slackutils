#!/bin/env python3

import glob
import os
import pkg_resources
import re
import readline
import shutil
import stat
import subprocess
import sys
import time

# Software Data:
soft_name = "Slackstack"
soft_tag  = "a slackbuild utility"

# Version
soft_vers = "0.8.9"


def hello_string():
    os.system("clear")
    welstr = ("Welcome to " + soft_name + " version " + soft_vers + ", " + soft_tag + ".")
    print("\n" + welstr)
    print("")


hello_string()
 
# This is where we set the path for a personal repo, slackbuilds in here get priority
dir_personal   = os.path.join(os.environ['HOME'], "slackware", "dbs_slackware", "")
# This is the path where slackstack assembles the builds
dir_stack      = os.path.join(os.environ['HOME'], "slackstack", "")
# This is where the local slackbuilds git repo is stored
dir_git        = os.path.join(os.environ['HOME'], "slackstack", "slackbuilds", "")

try:
    os.mkdir(os.path.join(dir_stack))
except(FileExistsError):
    pass

if os.path.isdir(os.path.join(dir_stack, "slackbuilds", "")):
    print("Found " + os.path.join(dir_stack, "slackstack", ""))
    print("Performing git pull...")
    git_fail = (subprocess.call(["git", "-C", os.path.join(dir_stack, "slackbuilds", ""), "pull"]))
    if git_fail > 0:
        time.sleep(2)
        hello_string()
        print("Found local Slackbuild repo but can't update. Moving on.")
    else:
        time.sleep(1)
        hello_string()
        print("Local Slackbuild repo up to date.")
else:
    print("Local copy of slackbuilds git not found in " + os.path.join(dir_stack, ""))
    make_local_git = input("Clone it now? y/n ")
    if make_local_git == "y" or make_local_git == "Y":
        git_fail = (subprocess.call(["git", "clone", "https://gitlab.com/SlackBuilds.org/slackbuilds.git", os.path.join(dir_stack, "slackbuilds", "")]))
        if git_fail > 0:
            print("\nCan't create a local Slackbuilds repo.  Do you have internet?\n")
            exit(1)
        else:
            time.sleep(1)
            hello_string()
            print("Local Slackbuild repo up to date.")
    else:
        print("Please create a local clone to use slackstack")
        exit(1)

check_path = glob.glob(os.path.join(os.environ['HOME'], "slackstack", "*tree", ""))
if check_path:
    check_path = (check_path[0].strip())
    print("\nFound a previous build:", check_path)
    remove_or_quit = input("(r)emove or (q)uit? ")
    if remove_or_quit == "R" or remove_or_quit == "r":
        shutil.rmtree(os.path.join(check_path))
    else:
        exit(1)

prog_base      = input("\nWhat program are we building? ")
prog_name      = prog_base.strip()
prog_build_dir = (prog_name + "-tree")

dir_path = os.path.join(os.environ['HOME'], "slackstack", prog_build_dir, "")
print("\nBuild directory =", dir_path)

# Make a list of SBo software categories
sbo_dirs = []
for name in os.listdir(dir_git):
    if os.path.isdir(os.path.join(dir_git, name)) is True:
        if "." not in name:
            sbo_dirs.append(name.strip())
sbo_dirs.sort()

list1_checked_for_deps = []
list2_is_a_dep = []
list3_install_seq = []

path_to_prog = os.path.join(dir_personal + prog_name)
if os.path.isdir(path_to_prog):
    try:
        shutil.copytree(os.path.join(path_to_prog), os.path.join(dir_path, prog_name))
    except FileExistsError:
        pass
else:
    for dir in sbo_dirs:
        path_to_prog = (dir_git + dir + "/" + prog_name)
        if os.path.isdir(path_to_prog):
            try:
                shutil.copytree(os.path.join(path_to_prog), os.path.join(dir_path, prog_name))
            except FileExistsError:
                pass


def get_version_of_prog_name():
    infofile = glob.glob(os.path.join(dir_path, prog_name, "*.info"))
    global version_prog_name
    if infofile:
        infofile = infofile[0]
        with open(infofile) as gvoc:
            infofile = gvoc.read()
        gvoc.closed
        for line in infofile.split("\n"):
            if "VERSION=" in line:
                version_prog_name = line.strip()
                version_prog_name = version_prog_name.split('"')[1]


def get_version_of_dep():
    infofile = glob.glob(os.path.join(dir_path, dep, "*.info"))
    global version_dep
    if infofile:
        infofile = infofile[0]
        with open(infofile) as gvoc:
            infofile = gvoc.read()
        gvoc.closed
        for line in infofile.split("\n"):
            if "VERSION=" in line:
                version_dep = line.strip()
                version_dep = version_dep.split('"')[1]


def iterate_for_dependecies():
    for dir in os.listdir(os.path.join(dir_path)):
        prog_name = dir
        prog_name = str(prog_name)

        if prog_name != "" and prog_name not in list1_checked_for_deps:
            list1_checked_for_deps.append(prog_name)
            infofile = glob.glob(os.path.join(dir_path, prog_name, "*.info"))
            if infofile:
                infofile = infofile[0]
                with open(infofile) as i:
                    infofile = i.read()
                i.closed

                for line in infofile.split("\n"):
                    if "REQUIRES=" in line:
                        depends = line.strip()
                        depends = depends.split('"')[1]
                        for dep in depends.split(" "):
                            list2_is_a_dep.append(dep)

                for item in list2_is_a_dep:
                    prog_name = item
                    path_to_prog = os.path.join(dir_personal + prog_name)
                    if os.path.isdir(path_to_prog):
                        try:
                            shutil.copytree(os.path.join(path_to_prog), os.path.join(dir_path, prog_name))
                        except FileExistsError:
                            pass
                    else:
                        for dir in sbo_dirs:
                            path_to_prog = os.path.join(dir_git + dir + "/" + prog_name)
                            if os.path.isdir(path_to_prog):
                                try:
                                    shutil.copytree(os.path.join(path_to_prog), os.path.join(dir_path, prog_name))
                                except FileExistsError:
                                    pass


def iterate_for_permissions():
    for dir in os.scandir(os.path.join(dir_path)):
        prog_name = dir
        buildfile = glob.glob(os.path.join(dir_path, prog_name, "*.SlackBuild"))
        if buildfile:
            buildfile = buildfile[0]
            os.chmod(os.path.join(buildfile), ( stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH ))


for w in range(10):
    try:
        iterate_for_dependecies()
    except FileNotFoundError:
        print("\nPlease check spelling and CAPS, --> " + prog_name + " <-- was not found in " + dir_git + ". \n")
        exit(1)

iterate_for_permissions()

print("\nAdding dependencies for: " + prog_name + "\n")
for dep in list2_is_a_dep[::-1]:
    if dep:
        if dep not in list3_install_seq:
            list3_install_seq.append(dep.lower())
list3_install_seq.append(prog_name)

app_data_search = re.compile("-[^a-z]+[\S]*[a-z]*")
app_ver_search = re.compile('-[x|n].*')
app_tag_search = re.compile("_\w+$")

# Dictionary of installed programs and version numbers
package_dict = {}
for p in os.listdir("/var/log/packages/"):
    app_data_match = app_data_search.search(p)
    app_name = p.replace(app_data_match.group(0), "")
    # try:
    app_arch_match = app_ver_search.search(app_data_match.group(0))
    if app_arch_match is not None:
        app_vers = app_data_match.group(0).replace(app_arch_match.group(0), "").lstrip("-")
    else:
        app_vers = app_data_match
        app_vers = app_vers.group(0)
    app_tag_match = app_tag_search.search(p)
    if app_tag_match is not None:
        app_tag = app_tag_match.group(0).lstrip("_")
        app_vers = (app_vers + " (" + app_tag + ")")
    else:
        app_vers = app_vers
    package_dict.update([(app_name.lower(),app_vers)])

# Dictionary of python programs and versions
python_dict  = {}
for i in pkg_resources.working_set:
    i = str(i).split()
    if i[0] not in python_dict:
        python_dict.update([(i[0].lower(),i[1])])

# Start the search
f = open(os.path.join(os.environ['HOME'], dir_path, "installseq.txt"), "a")
f.write("Install order:\n")
for dep in list3_install_seq:
    if dep:
        if package_dict.get(dep) is not None:
            dep_vers = package_dict.get(dep)
            get_version_of_dep()
            dep_status = ("--> [INSTALLED] version is " + dep + " " + package_dict.get(dep))
            print(dep + " " + version_dep)
            print(dep_status)
            print("")
            f.write(dep + " " + version_dep + " " + dep_status + "\n")
        elif python_dict.get(dep) is not None and package_dict.get(dep) is None:
            dep_vers = python_dict.get(dep)
            get_version_of_dep()
            dep_status = ("--> [INSTALLED] version is " + dep + " " + python_dict.get(dep))
            print(dep + " " + version_dep)
            print(dep_status)
            print("")
            f.write(dep + " " + version_dep + " " + dep_status + "\n")
        elif "python" in dep and dep != "python3":
            dep_base_check = dep.split("-")
            if dep_base_check[1] == "python" or dep_base_check[1] == "python3":
                dep_base_check = str(dep_base_check[0].rstrip("0123456789"))
                if dep_base_check in python_dict:
                    get_version_of_dep()
                    dep_status = ("--> [INSTALLED] version is " + dep + " " + python_dict.get(dep_base_check))
                    print(dep + " " + version_dep)
                    print(dep_status)
                    print("")
                    f.write(dep + " " + version_dep + " " + dep_status + "\n")
            if dep_base_check[0] == "python" or dep_base_check[0] == "python3":
                dep_base_check = str(dep_base_check[1].rstrip("0123456789"))
                if dep_base_check in python_dict:
                    get_version_of_dep()
                    dep_status = ("--> [INSTALLED] version is " + dep + " " + python_dict.get(dep_base_check))
                    print(dep + " " + version_dep)
                    print(dep_status)
                    print("")
                    f.write(dep + " " + version_dep + " " + dep_status + "\n")
                else:
                    get_version_of_dep()
                    print(dep + " " + version_dep)
                    print("")
                    f.write(dep + " " + version_dep + "\n")
        elif "py" in dep and "python" not in dep:
            dep_soft_check = ''.join([letter for letter in dep if not letter.isdigit()])
            if dep_soft_check in python_dict:
                get_version_of_dep()
                dep_status = ("--> [MAY BE INSTALLED] version is " + dep_soft_check + " " + python_dict.get(dep_soft_check))
                print(dep + " " + version_dep)
                print(dep_status)   
                print("")
                f.write(dep + " " + version_dep + " " + dep_status + "\n")
            else:
                get_version_of_dep()
                print(dep + " " + version_dep)
                print("")
                f.write(dep + " " + version_dep + "\n")
        else:
            get_version_of_dep()
            print(dep + " " + version_dep)
            print("")
            f.write(dep + " " + version_dep + "\n")
f.close()

print("\nto", dir_path, "\n")

grab_y_n = input("Run slackgrab.py to get the tarballs (y/n)? ")
if grab_y_n == "Y" or grab_y_n == "y":
    progpath = sys.path[0]
    progpath_list = []
    for item in (os.listdir(path=progpath)):
        progpath_list.append(item)
    if "slackgrab.py" in progpath_list:
        subprocess.run(["slackgrab.py", "--skip"])
        exit(0)
    else:
        print("")
        print("Missing slackgrab.py script!")
        print("Please make sure it is in the same dir as slackstack.py")
        print("")
        exit(1)
else:
    exit(0)
