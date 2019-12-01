#!/bin/env python3

# Version 0.5.2

import os
import shutil
import glob
import stat

os.system("clear")

prog_base      = input("\nWhat program are we building? ")
prog_name      = prog_base.strip()
prog_build_dir = prog_base + "-tree"

try:
    os.mkdir(os.path.join(os.environ['HOME'], "slackstack"))
except FileExistsError:
    check_path = os.path.join(os.environ['HOME'], "slackstack")
    for dir in os.scandir(check_path):
        path_name = str(dir).split("'")[1]
        print("\nThe build directory contains: ", path_name)
        remove_or_quit = input("(r)emove or (q)uit? ")
        if remove_or_quit == "R" or remove_or_quit == "r":
            shutil.rmtree(os.path.join(check_path, path_name))
        else:
            exit(1)

print("\n" + "What directory will we pull packages from?")
print("\t" + "1 = dev_slack15 (development)" + "\n" + "\t" + "2 = slackbuilds (SBo)")
prog_src_dir = 0
while prog_src_dir == 0:
    src_in = input("Selection or (q)uit: ")
    if src_in == "q" or src_in == "Q":
        print("quitting" + "\n")
        exit(0)
    elif src_in == "1":
        prog_src_dir = "slackware/dev_slack15"
    elif src_in == "2":
        prog_src_dir = "slackbuilds"
    else:
        print("Please select a number or (q)uit")
        continue
# dir_personal   = os.path.join(os.environ['HOME'], "slackware", src_dir, "")
# dir_git        = os.path.join(os.environ['HOME'], "slackbuilds", "")
src_path       = os.path.join(os.environ['HOME'], prog_src_dir, "")
bld_path       = os.path.join(os.environ['HOME'], "slackstack", prog_build_dir, "")

print("\nBuild directory =", os.path.join(os.environ['HOME'], bld_path, ""))

dirs = ['academic',
        'accessibility',
        'audio',
        'business',
        'desktop',
        'development',
        'games',
        'gis',
        'graphics',
        'ham',
        'haskell',
        'libraries',
        'misc',
        'multimedia',
        'network',
        'office',
        'perl',
        'python',
        'ruby',
        'system']

list1_checked_for_deps = []
list2_is_a_dep = []
list3_install_seq = []

# path_to_prog = os.path.join(src_path + prog_name)
# if os.path.isdir(path_to_prog):
#     print("\nFound", os.path.join(path_to_prog))
#     try:
#         shutil.copytree(os.path.join(path_to_prog), os.path.join(bld_path, prog_name))
#     except FileExistsError:
#         pass
# else:
for dir in dirs:
    path_to_prog = (src_path + dir + "/" + prog_name)
    if os.path.isdir(path_to_prog):
        print("\nSource:", os.path.join(path_to_prog))
        try:
            shutil.copytree(os.path.join(path_to_prog), os.path.join(bld_path, prog_name))
        except FileExistsError:
            pass

#list1_checked_for_deps.append(prog_name)
def iterate_for_dependecies():
    for dir in os.listdir(os.path.join(bld_path)):
        prog_name = dir
        prog_name = str(prog_name)

        if prog_name != "" and prog_name not in list1_checked_for_deps:
            list1_checked_for_deps.append(prog_name)
#            print(prog_name)

            infofile = glob.glob(os.path.join(bld_path, prog_name, "*.info"))
            if infofile:
                infofile = infofile[0]

                with open(infofile) as i:
                    infofile = i.read()
                i.closed

                for line in infofile.split("\n"):
                    if "REQUIRES=" in line:
                        depends = line.strip()
                        depends = depends.split('"')[1]
#                        print("\nThis software requires:")
                        for dep in depends.split(" "):
#                            print("-->", dep)
                            #if dep not in list2_is_a_dep:
                            list2_is_a_dep.append(dep)

                for item in list2_is_a_dep:
                    prog_name = item
#                     path_to_prog = os.path.join(src_path + dir + "/" + prog_name)
#                     # path_to_prog = os.path.join(src_path + prog_name)
# #                    print(path_to_prog)
#                     if os.path.isdir(path_to_prog):
# #                        print(os.path.join(path_to_prog))
# #                        print("YES")
#                         try:
#                             shutil.copytree(os.path.join(path_to_prog), os.path.join(bld_path, prog_name))
#                         except FileExistsError:
#                             pass
# #                         #if prog_name not in list1_checked_for_deps:
# #                         list1_checked_for_deps.append(prog_name)
                    # else:
                    for dir in dirs:
                        path_to_prog = os.path.join(src_path + dir + "/" + prog_name)
                        if os.path.isdir(path_to_prog):
 #                           print(os.path.join(path_to_prog))
 #                           print("YES")
                            try:
                                shutil.copytree(os.path.join(path_to_prog), os.path.join(bld_path, prog_name))
                            except FileExistsError:
                                pass
                            #if prog_name not in list1_checked_for_deps:
#                                 list1_checked_for_deps.append(prog_name)

def iterate_for_permissions():
    for dir in os.scandir(os.path.join(bld_path)):
        prog_name = dir
        buildfile = glob.glob(os.path.join(bld_path, prog_name, "*.SlackBuild"))
        if buildfile:
            buildfile = buildfile[0]
            os.chmod(os.path.join(buildfile), ( stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH ))

for w in range(10):
    iterate_for_dependecies()

iterate_for_permissions()

# print("\nCHECKED FOR DEPS")
# print(*list1_checked_for_deps,  sep="\n")
# print("\nIS A DEP")
# print(*list2_is_a_dep, sep="\n")
# print("\n")

print("\nAdding dependencies:")
for dep in list2_is_a_dep[::-1]:
    if dep not in list3_install_seq:
        list3_install_seq.append(dep)

f = open(os.path.join(os.environ['HOME'], bld_path, "installseq.txt"), "a")
for dep in list3_install_seq:
    if dep:
        if os.path.isdir(os.path.join(bld_path, dep)):
            print(dep)
            f.write(dep + "\n")
print("\nto", bld_path, "\n")
f.write(prog_base)
f.close()
