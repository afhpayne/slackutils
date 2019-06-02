#!/bin/env python3

# Version 0.4.0

import os
import shutil
import glob
import stat

os.system("clear")
prog_base      = input("\nWhat program are we building? ")
prog_name      = prog_base.strip()
prog_build_dir = prog_base + "-tree"
dir_personal   = os.path.join(os.environ['HOME'], "slackware", "slackbuilds15", "")
dir_git        = os.path.join(os.environ['HOME'], "slackbuilds", "")
dir_path       = os.path.join(os.environ['HOME'], "Desktop", prog_build_dir, "")
try:
    os.mkdir(os.path.join(os.environ['HOME'], "Desktop", prog_build_dir))
except FileExistsError:
    os.rename(os.path.join(os.environ['HOME'], "Desktop", prog_build_dir), os.path.join(os.environ['HOME'], "Desktop", prog_build_dir + ".old"))
    os.mkdir(os.path.join(os.environ['HOME'], "Desktop", prog_build_dir))
print("\nBuild directory =", os.path.join(os.environ['HOME'], "Desktop", prog_build_dir, ""))

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

dependency_checked = []
dependency_list = []

path_to_prog = os.path.join(dir_personal + prog_name)
if os.path.isdir(path_to_prog):
    print("\nFound", os.path.join(path_to_prog))
    try:
        shutil.copytree(os.path.join(path_to_prog), os.path.join(dir_path, prog_name))
    except FileExistsError:
        pass
else:
    for dir in dirs:
        path_to_prog = (dir_git + dir + "/" + prog_name)
        if os.path.isdir(path_to_prog):
            print("\nFound:", os.path.join(path_to_prog))
            try:
                shutil.copytree(os.path.join(path_to_prog), os.path.join(dir_path, prog_name))
            except FileExistsError:
                pass

#dependency_checked.append(prog_name)
def iterate_for_dependecies():
    for dir in os.scandir(os.path.join(dir_path)):
        prog_name = dir

        if prog_name != "" and prog_name not in dependency_checked:
#            print(prog_name)

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
#                        print("\nThis software requires:")
                        for dep in depends.split(" "):
#                            print("-->", dep)
                            if dep not in dependency_list:
                                dependency_list.append(dep)

                for item in dependency_list:
                    prog_name = item
                    path_to_prog = os.path.join(dir_personal + prog_name)
#                    print(path_to_prog)
                    if os.path.isdir(path_to_prog):
#                        print(os.path.join(path_to_prog))
#                        print("YES")
                        try:
                            shutil.copytree(os.path.join(path_to_prog), os.path.join(dir_path, prog_name))
                        except FileExistsError:
                            pass
                        if prog_name not in dependency_checked:
                            dependency_checked.append(prog_name)
                    else:
                        for dir in dirs:
                            path_to_prog = os.path.join(dir_git + dir + "/" + prog_name)
                            if os.path.isdir(path_to_prog):
 #                               print(os.path.join(path_to_prog))
 #                               print("YES")
                                try:
                                    shutil.copytree(os.path.join(path_to_prog), os.path.join(dir_path, prog_name))
                                except FileExistsError:
                                    pass
                                if prog_name not in dependency_checked:
                                    dependency_checked.append(prog_name)

def iterate_for_permissions():
    for dir in os.scandir(os.path.join(dir_path)):
        prog_name = dir
        buildfile = glob.glob(os.path.join(dir_path, prog_name, "*.SlackBuild"))
        if buildfile:
            buildfile = buildfile[0]
            os.chmod(os.path.join(buildfile), ( stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH ))

for w in range(10):
    iterate_for_dependecies()
print(dependency_checked)

iterate_for_permissions()

f = open(os.path.join(os.environ['HOME'], "Desktop", prog_build_dir, "installseq.txt"), "a")
print("\nAdding dependencies:")
for dep in dependency_list[::-1]:
    if dep:
        if os.path.isdir(os.path.join(dir_path, dep)):
            print(dep)
            f.write(dep + "\n")
print("\nto", dir_path, "\n")
f.write(prog_base)
f.close()
