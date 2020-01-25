### Slackutils

The goal of Slackutils is to make working with slackbuilds easier.

#### There are two utilities -- slackstack and slackgrab

#### Slackstack:<br />
Uses a local clone of the slackbuilds.org git repository <br />
1. Searches for a program in the local clone or user folder<br />
2. Copies the slackbuild to a 'build' directory --> default = ~/slackstack/[program_name]-tree<br />
3. Scans the slackbuild for dependencies and copies *those* slackbuilds to the build directory<br />
4. Recursively scans all dependencies for additional dependencies... and so on until every *needed* slackbuild has been copied to the build directory<br />
5. Creates a text file to show the installation order of the slackbuilds
6. Sets the *.SlackBuild file permissions in each folder to executable

#### Slackgrab:  
1. Asks if the user wants to iterate through all folders in build directory (see above) to identify needed tar files<br />
2. Downloads the 64-bit tar files to the matching slackbuild directory<br />
3. Verifies the MD5sum for the downloaded files against the one in the respective *.info files
4. Allows the user to use the default build location (/home/user/slackstack) or to choose another

Everything is written in python 3.8 and has no dependencies beyond the standard python library.

#### Release Notes:<br />
__0.6.1__ slackstack now searches the local __python library__ to see if the program being built or its dependencies are already installed.  If /var/lib/pkgtools/packages/ doesn't contain a search hit, slackstack uses Python's pkg_resources tool to search local pip files.  This search is pretty robust; it will first look for exact hits and if none are found it performs a second fuzzier search.<br />
* Python libraries in the SBo have some naming oddities that slackstack handles.  For example, if the slackbuild calls for python3-Flask, slackstack knows to search for "Flask" since the former will return no hit even if Flask is actually installed via pip.  It doesn't matter if the order is reversed either, as with gst-python3.<br />
* The fuzzy search is meant to alert the user to scenarios like py3cairo vs pycairo -- if the slackbuild calls for py3cairo, slackstack will alert the user that pycairo is installed and they can determine for themselves if the dependency is met.<br />
* Version numbers are now shown.  If slackstack finds the program it's building or a dependency already installed, it shows the version number of the installed program.<br />

__0.5.3__ slackstack has one important new feature -- now it searches the computer to see if the program being built or its dependencies are already installed.  In either case, it adds asterisks to the relevant entries in the installseq.txt file and shows [INSTALLED] on the screen output.

__0.5.0__ slackgrab is a major revision.  The code is cleaner and handles *.info files in a more efficient manner.<br />
* Programs with multiple (unlimited) binaries are now supported.  This means things like the Nvidia driver are downloaded and verified correctly<br />
* The code now supports slackbuild *.info files where the tarball htmls are located in either the DOWNLOADS_x86_64 area or the DOWNLOADS area.  There is some variation among slackbuilds, so the program checks the x86 location first and moves to the other one if nothing is found.

Near-term goals:<br />
* [DONE] add support for local pip libraries
* [DONE] add support for multiple binary builds
* combine utilities into one program
* [DONE] Add user input to select directories<br />
* [DONE] Add slackgrab option to traverse multiple slackbuild directories and download tar files for each<br />
* [PHASE1] Maybe add 32-bit support<br />
* [DONE] Search a local database for available slackbuilds (e.g., a local git clone of the slackbuilds repo)<br />
* Search a remote database for available slackbuilds (e.g., slackbuilds.org)<br />

