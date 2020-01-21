#!/bin/env python3


import pkg_resources

# dists = []

# dists = [d for d in pkg_resources.working_set]

# for i in dists:
#     if "pygobject3-python3" in str(i):
#         print(i)
#         if i:
#             print("YES")
#         else:
#             print("NO")

# THIS SECTION IS THE PIP SEARCH
pip_trace_list = []
prog_base = prog_base.split("-")
if prog_base[1] == "python" or prog_base[1] == "python3":
    prog_base = str(prog_base[0])
else:
    prog_base = str(prog_base[1])
l = []
pip_trace = [i for i in pkg_resources.working_set]
for j in pip_trace:
    k = str(j)
    l.append(k)
for m in l:
    m = m.split(" ")
    m.pop()
    for n in m:
        pip_trace_list.append(n.strip())

print(pip_trace_list)
exit()    
