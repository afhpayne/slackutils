#!/bin/env python3

# MIT License

# Copyright (c) 2019-2020 Andrew Payne

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
soft_vers = "0.9.4"

# This is where we set the path for personal repos, paths here get priority
# First priority
dir_dev = os.path.join(
    os.environ['HOME'], "slackware", "dev_slack", "")
# Second priority
dir_dbs = os.path.join(
    os.environ['HOME'], "slackware", "dbs_slackware", "")
# This is the path where slackstack assembles the builds
dir_stack = os.path.join(
    os.environ['HOME'], "slackstack", "")
# This is where the local slackbuilds git repo is stored
dir_git = os.path.join(
    os.environ['HOME'], "slackstack", "slackbuilds", "")


def hello_string():
    os.system("clear")
    welstr = ("Welcome to " + soft_name + " version "
              + soft_vers + ", " + soft_tag + ".")
    print("\n" + welstr)
    print("")


def make_slackstack_dir_func():
    try:
        os.mkdir(os.path.join(dir_stack))
    except(FileExistsError):
        pass


def clone_repo_func():
    if os.path.isdir(os.path.join(dir_stack, "slackbuilds", "")):
        print("Found " + os.path.join(dir_stack, "slackstack", ""))
        print("Performing git pull...")
        git_fail = (subprocess.call(
            ["git", "-C", os.path.join(dir_stack, "slackbuilds", ""), "pull"])
                    )
        if git_fail > 0:
            time.sleep(2)
            hello_string()
            print("Found local Slackbuild repo but can't update.")
            print("Do you have internet? Using repo as is....")
        else:
            time.sleep(1)
            hello_string()
            print("Local Slackbuild repo up to date.")
    else:
        print("Local copy of slackbuilds git not found in "
              + os.path.join(dir_stack, ""))
        make_local_git = input("Clone it now? y/n ")
        if make_local_git == "y" or make_local_git == "Y":
            git_fail = (subprocess.call(
                ["git", "clone",
                 "https://gitlab.com/SlackBuilds.org/slackbuilds.git",
                 os.path.join(dir_stack, "slackbuilds", "")])
                        )
            if git_fail > 0:
                print("\nCan't create a local Slackbuilds repo.")
                print("Do you have internet? Exiting...\n")
                exit(1)
            else:
                time.sleep(1)
                hello_string()
                print("Local Slackbuild repo up to date.")
        else:
            print("Please create a local clone to use slackstack")
            exit(1)


def check_for_old_build_func():
    check_path = glob.glob(
        os.path.join(os.environ['HOME'], "slackstack", "*tree", ""))
    if check_path:
        check_path = (check_path[0].strip())
        print("\nFound a previous build:", check_path)
        remove_or_quit = input("(r)emove or (q)uit? ")
        if remove_or_quit == "R" or remove_or_quit == "r":
            shutil.rmtree(os.path.join(check_path))
        else:
            exit(1)


def make_sbo_dir_list_func():
    for name in os.listdir(dir_git):
        if os.path.isdir(os.path.join(dir_git, name)) is True:
            if "." not in name:
                sbo_dirs.append(name.strip())
    sbo_dirs.sort()


def make_build_tree_func():
    x = 0
    for path in os.walk(dir_dev):
        if os.path.isdir(path[0]) and prog_name == (
                path[0].split("/")[-1]):
            prog_build_dir = (prog_name + "-tree")
            x = 1
        else:
            pass
    for path in os.walk(dir_dbs):
        if x == 0 and os.path.isdir(path[0]) and prog_name == (
                path[0].split("/")[-1]):
            prog_build_dir = (prog_name + "-tree")
            x = 1
        else:
            pass
    for path in os.walk(dir_git):
        if x == 0 and os.path.isdir(path[0]) and prog_name == (
                path[0].split("/")[-1]):
            prog_build_dir = (prog_name + "-tree")
            x = 1
        else:
            pass
    if x == 0:
        print("\nCouldn't find " + prog_name + ", exiting...\n")
        exit()
    else:
        prog_build_path.append(os.path.join(dir_stack, prog_build_dir))
        print("\nBuild path is " + prog_build_path[0])
        os.mkdir(prog_build_path[0])


def copy_to_build_dir_func():
    path_to_prog = os.path.join(dir_dbs + prog_name)
    path_to_build = os.path.join(prog_build_path[0] + "/")
    if os.path.isdir(path_to_prog):
        try:
            shutil.copytree(path_to_prog, path_to_build + prog_name)
        except FileExistsError:
            pass
    path_to_prog = os.path.join(dir_dev + prog_name)
    if os.path.isdir(path_to_prog):
        try:
            shutil.copytree(path_to_prog, path_to_build + prog_name)
        except FileExistsError:
            pass
    else:
        for dir in sbo_dirs:
            path_to_prog = (dir_git + dir + "/" + prog_name)
            if os.path.isdir(path_to_prog):
                try:
                    shutil.copytree(path_to_prog, path_to_build + prog_name)
                except FileExistsError:
                    pass


def iterate_for_dependencies():
    path_to_build = os.path.join(prog_build_path[0] + "/")
    for directory in os.listdir(path_to_build):
        prog_name = directory

        if prog_name != "" and prog_name not in list1_checked_for_deps:
            list1_checked_for_deps.append(prog_name)
            infofile = glob.glob(
                os.path.join(path_to_build, prog_name, "*.info"))
            if infofile:
                infofile = infofile[0]
                with open(infofile) as i:
                    infofile = i.read()

                for line in infofile.split("\n"):
                    if "REQUIRES=" in line:
                        depends = line.strip()
                        depends = depends.split('"')[1]
                        for dep in depends.split(" "):
                            list2_is_a_dep.append(dep)


def copy_dependencies_func():    
    for item in list2_is_a_dep:
        prog_name = item
        path_to_prog = os.path.join(dir_dbs + prog_name)
        path_to_build = os.path.join(prog_build_path[0] + "/")
        if os.path.isdir(path_to_prog):
            try:
                shutil.copytree(
                    path_to_prog, path_to_build + prog_name
                )
            except FileExistsError:
                pass
        path_to_prog = os.path.join(dir_dev + prog_name)
        if os.path.isdir(path_to_prog):
            try:
                shutil.copytree(
                    path_to_prog, path_to_build + prog_name
                )
            except FileExistsError:
                pass
        else:
            for dir in sbo_dirs:
                path_to_prog = (dir_git + dir + "/" + prog_name)
                if os.path.isdir(path_to_prog):
                    try:
                        shutil.copytree(
                            path_to_prog, path_to_build + prog_name
                        )
                    except FileExistsError:
                        pass


def iterate_for_permissions():
    path_to_build = os.path.join(prog_build_path[0] + "/")
    for directory in os.scandir(path_to_build):
        prog_name = directory
        buildfile = glob.glob(os.path.join(
            path_to_build, prog_name, "*.SlackBuild")
                              )
        if buildfile:
            buildfile = buildfile[0]
            os.chmod(os.path.join(buildfile), (
                stat.S_IRUSR |
                stat.S_IWUSR |
                stat.S_IXUSR |
                stat.S_IRGRP |
                stat.S_IXGRP |
                stat.S_IROTH |
                stat.S_IXOTH )
                     )


def show_dependency_list_func():
    print("\nAdding dependencies for: " + prog_name + "\n")
    for dep in list2_is_a_dep[::-1]:
        if dep:
            if dep not in list3_install_seq:
                list3_install_seq.append(dep.lower())
    list3_install_seq.append(prog_name)


def make_dict_of_packages_func():
    app_data_search = re.compile("-[^a-z]+[\S]*[a-z]*")
    app_ver_search = re.compile('-[x|n].*')
    app_tag_search = re.compile("_\w+$")

    for item in os.listdir("/var/log/packages/"):
        app_data_match = app_data_search.search(item)
        app_name = item.replace(app_data_match.group(0), "")
        # try:
        app_arch_match = app_ver_search.search(app_data_match.group(0))
        if app_arch_match is not None:
            app_vers = app_data_match.group(0).replace(
                app_arch_match.group(0), "").lstrip("-")
        else:
            app_vers = app_data_match
            app_vers = app_vers.group(0)
        app_tag_match = app_tag_search.search(item)
        if app_tag_match is not None:
            app_tag = app_tag_match.group(0).lstrip("_")
            app_vers = (app_vers + " (" + app_tag + ")")
        else:
            app_vers = app_vers
        package_dict.update([(app_name.lower(),app_vers)])


def make_dict_of_python_packages_func():
    for item in pkg_resources.working_set:
        item = str(item).split()
        if item[0] not in python_dict:
            python_dict.update([(item[0].lower(),item[1])])


def get_version_of_dep():
    for dep in list3_install_seq:
        infofile = glob.glob(os.path.join(prog_build_path[0], dep, "*.info"))
        if infofile:
            infofile = infofile[0]
            with open(infofile) as gvoc:
                infofile = gvoc.read()
            for line in infofile.split("\n"):
                if "VERSION=" in line:
                    version_dep = line.strip()
                    version_dep = version_dep.split('"')[1]
                    version_dep_list.clear()
                    version_dep_list.append(version_dep)


def create_install_list_func():
    with open(os.path.join(
            os.environ['HOME'], prog_build_path[0], "installseq.txt"),
              "a") as f:
        f.write("Install order:\n")


def dep_is_installed_func():
    for dep in list3_install_seq:
        if dep not in list4_deps_done:
            if package_dict.get(dep) is not None:
                dep_vers = package_dict.get(dep)
                get_version_of_dep()
                dep_status = ("--> [INSTALLED] version is "
                              + dep
                              + " "
                              + package_dict.get(dep)
                              )
                print(dep + " " + version_dep_list[0])
                print(dep_status)
                print("")
                list4_deps_done.append(dep)
                with open(os.path.join(
                        os.environ['HOME'], prog_build_path[0],
                        "installseq.txt"), "a") as f:
                    f.write(dep + " " + version_dep_list[0] + " "
                            + dep_status + "\n")


def dep_is_python_var1_func():
    for dep in list3_install_seq:
        if dep not in list4_deps_done:
            if python_dict.get(dep) is not None and \
               package_dict.get(dep) is None:
                dep_vers = python_dict.get(dep)
                get_version_of_dep()
                dep_status = ("--> [INSTALLED] version is "
                              + dep
                              + " "
                              + python_dict.get(dep)
                              )
                print(dep + " " + version_dep_list[0])
                print(dep_status)
                print("")
                list4_deps_done.append(dep)
                with open(os.path.join(
                        os.environ['HOME'], prog_build_path[0],
                        "installseq.txt"), "a") as f:
                    f.write(dep + " " + version_dep_list[0] + " "
                            + dep_status + "\n")


def dep_is_python_var2_func():
    for dep in list3_install_seq:
        if dep not in list4_deps_done:
            if "python" in dep and dep != "python3":
                try:
                    dep_base_check = dep.split("-")
                    if dep_base_check[1] == "python" or \
                       dep_base_check[1] == "python3":
                        dep_base_check = str(
                            dep_base_check[0].rstrip("0123456789")
                        )
                        if dep_base_check in python_dict:
                            get_version_of_dep()
                            dep_status = ("--> [INSTALLED] version is "
                                          + dep
                                          + " "
                                          + python_dict.get(dep_base_check)
                                          )
                            print(dep + " " + version_dep_list[0])
                            print(dep_status)
                            print("")
                            list4_deps_done.append(dep)
                            with open(os.path.join(
                                    os.environ['HOME'], prog_build_path[0],
                                    "installseq.txt"), "a") as f:
                                f.write(dep + " " + version_dep_list[0] + " "
                                        + dep_status + "\n")
                except(IndexError):
                    continue


def dep_is_python_var3_func():
    for dep in list3_install_seq:
        if dep not in list4_deps_done:
            dep_base_check = dep.split("-")
            if dep_base_check[0] == "python" or \
               dep_base_check[0] == "python3":
                try:
                    dep_base_check = str(
                        dep_base_check[1].rstrip("0123456789")
                    )
                    if dep_base_check in python_dict:
                        get_version_of_dep()
                        dep_status = ("--> [INSTALLED] version is "
                                      + dep
                                      + " "
                                      + python_dict.get(dep_base_check)
                                      )
                        print(dep + " " + version_dep_list[0])
                        print(dep_status)
                        print("")
                        list4_deps_done.append(dep)
                        with open(os.path.join(
                                os.environ['HOME'], prog_build_path[0],
                                "installseq.txt"), "a") as f:
                            f.write(dep + " " + version_dep_list[0] + " "
                                    + dep_status + "\n")
                except(IndexError):
                    continue


def dep_is_python_soft_func():
    for dep in list3_install_seq:
        if dep not in list4_deps_done:
            if "py" in dep and "python" not in dep:
                dep_soft_check = ''.join(
                    [letter for letter in dep if not letter.isdigit()]
                )
                if dep_soft_check in python_dict:
                    get_version_of_dep()
                    dep_status = ("--> [MAY BE INSTALLED] version is "
                                  + dep_soft_check
                                  + " "
                                  + python_dict.get(dep_soft_check)
                                  )
                    print(dep + " " + version_dep_list[0])
                    print(dep_status)   
                    print("")
                    list4_deps_done.append(dep)
                    with open(os.path.join(
                            os.environ['HOME'], prog_build_path[0],
                            "installseq.txt"), "a") as f:
                        f.write(dep + " " + version_dep_list[0] + " "
                                + dep_status + "\n")


def dep_is_not_installed_func():
    for dep in list3_install_seq:
        if dep not in list4_deps_done:
            dep_vers = package_dict.get(dep)
            get_version_of_dep()
            get_version_of_dep()
            print(dep + " " + version_dep_list[0])
            print("")
            list4_deps_done.append(dep)
            with open(os.path.join(
                    os.environ['HOME'], prog_build_path[0],
                    "installseq.txt"), "a") as f:
                f.write(dep + " " + version_dep_list[0] + "\n")


# Let's get started
hello_string()
make_slackstack_dir_func()
clone_repo_func()
check_for_old_build_func()

sbo_dirs = []
make_sbo_dir_list_func()

prog_base = input("\nWhat program are we building? ")
prog_name = prog_base.strip()

prog_build_path = []
make_build_tree_func()

copy_to_build_dir_func()

list1_checked_for_deps = []
list2_is_a_dep = []
for x in range(100):
    iterate_for_dependencies()
    copy_dependencies_func()

iterate_for_permissions()

list3_install_seq = []
show_dependency_list_func()

package_dict = {}
make_dict_of_packages_func()

python_dict  = {}
make_dict_of_python_packages_func()

# Start the list
create_install_list_func()

version_dep_list = []
list4_deps_done = []
dep_is_installed_func()
dep_is_python_var1_func()
dep_is_python_var2_func()
dep_is_python_var3_func()
dep_is_python_soft_func()
dep_is_not_installed_func()

print("\nto", prog_build_path[0], "\n")

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
