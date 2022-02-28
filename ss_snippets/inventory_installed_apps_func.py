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

import os

def inventory_installed_apps_func():
    installed_list = []
    installed_dict = {}
    number = 0
    for item in os.listdir("/var/log/packages/"):
        item = item.split(("-"))
        itembuild = item[-1].strip()
        # here we flag third party tagged software
        if len(item[-1]) > 3:
            itemversion = item[-3]+" ("+itembuild+")"
            if len(item) == 7:
                itemname = item[0]+"-"+item[1]+"-"+item[2]+"-"+item[3]
                installed_dict.update({itemname:itemversion})
                # installed_list.append(itemname+" "+itemversion)
            elif len(item) == 6:
                itemname = item[0]+"-"+item[1]+"-"+item[2]
                installed_dict.update({itemname:itemversion})
                # installed_list.append(itemname+" "+itemversion)
            elif len(item) == 5:
                itemname = item[0]+"-"+item[1]
                installed_dict.update({itemname:itemversion})
                # installed_list.append(itemname+" "+itemversion)
            else:
                itemname = item[0]
                installed_dict.update({itemname:itemversion})
                # installed_list.append(itemname+" "+itemversion)
        # no tag means it's in the base system
        else:
            itemversion = item[-3]
            if len(item) == 7:
                itemname = item[0]+"-"+item[1]+"-"+item[2]+"-"+item[3]
                installed_dict.update({itemname:itemversion})
                # installed_list.append(itemname+" "+itemversion)
            elif len(item) == 6:
                itemname = item[0]+"-"+item[1]+"-"+item[2]
                installed_dict.update({itemname:itemversion})
                # installed_list.append(itemname+" "+itemversion)
            elif len(item) == 5:
                itemname = item[0]+"-"+item[1]
                installed_dict.update({itemname:itemversion})
                # installed_list.append(itemname+" "+itemversion)
            else:
                itemname = item[0]
                installed_dict.update({itemname:itemversion})
                # installed_list.append(itemname+" "+itemversion)
    for item in os.listdir("/usr/bin/"):
        if item not in installed_list:
            installed_dict.update({item:"(version_unkown)"})
            # installed_list.append(item+" (version unknown)")
    for item in os.listdir("/usr/lib64"):
        if item[0:3] == "lib":
            itemname = item[3:].split(".")
            itemname = itemname[0]
            if itemname not in installed_list:
                installed_dict.update({itemname:"(system library)"})
                # installed_list.append(itemname+" (system library)")

            
    print(installed_dict)

inventory_installed_apps_func()

exit(1)

