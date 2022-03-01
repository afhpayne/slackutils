## Slackutils

The goal of Slackutils is to make working with slackbuilds easy.

#### There are two programs: __slackstack.py__ and __slackgrab.py__
If both programs are executable and in the same directory, slackstack.py can call slackgrab.py to automatically download tarballs.<br />

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

### Dependencies
Everything is written in Python 3.9 and has no dependencies beyond the standard python library.

### Release Notes for Slackstack:<br />
__0.10.4__ cleanup, fixed and improved installseq.txt<br />
__0.10.2__ clean up, git pull fixed<br />
__0.10.0__ major rewrite and refactor, transient version bug elminated, bug removal, simplify code.<br />
__0.9.5__ clean up code<br />
__0.9.3__ clean up code<br />
__0.9.2__ refactor and fix bugs<br />
__0.9.1__ refactor and fix scope bug<br />
__0.9.0__ added repo priority list<br />
__0.8.9__ Bug fix, cleanup<br />
__0.8.8__ Bug fix<br />
__0.8.7__ Made slackgrab call more robust.  Now slackstack.py will look for slackgrab.py in the launch directory.  Therefore these scripts need not be in an executable PATH.<br />
__0.8.6__ Added support for Slackgrab --skip argument.<br />
__0.8.5__ Moved local app search to /var/log/packages for compatibility with 14.2 and current.<br />
__0.8.4__ Code cleanup, also the SBo dirs list is no longer hardcoded but is now dynamically updated.  Slackstack now asks if the user wants to proceed to Slackgrab to get tarballs.<br />
__0.8.3__ Slackstack now reads tags.  Any custom tag on installed software is read and displayed.  This works for SBo software or custom tags (if you use them).  You can now see if something you wish to install will overwrite a base package.  If you're running -current, this is handy because SBo dependencies reference the 14.2 base system and a lot has been added to -current.<br />
__0.8.2__ Bug fixes and cleanup.<br />
__0.8.1__ Slackstack now clones the Slackbuild repo to the local drive and keeps it up-to-date with every launch.  Lack of internet is handled gracefully too.<br />
__0.8.0__ This is another major overhaul.  Slackstack's ability to correctly identify already installed software is improved: (1) it's faster and more a lot more efficient and (2) it's more robust.  Python libraries in particular are now much more reliably identified if the user has things in pip.  The visual layout is upgraded to allow easier comparison of requested vs. installed software versions too.<br />
__0.7.0__ Slackstack now shows the version of the software being sourced from your local slackbuilds git clone.  Now you'll see exactly what version you're about to build of the program you want and all its dependencies too.  Also Slackstack now handles a mispelled program request more gracefully.<br />
__0.6.2__ Bug fixes<br />
__0.6.1__ slackstack now searches the local __python library__ to see if the program being built or its dependencies are already installed.  If /var/lib/pkgtools/packages/ doesn't contain a search hit, slackstack uses Python's pkg_resources tool to search local pip files.  This search is pretty robust; it will first look for exact hits and if none are found it performs a second fuzzier search.<br />
* Python libraries in the SBo have some naming oddities that slackstack handles.  For example, if the slackbuild calls for python3-Flask, slackstack knows to search for "Flask" since the former will return no hit even if Flask is actually installed via pip.  It doesn't matter if the order is reversed either, as with gst-python3.<br />
* The fuzzy search is meant to alert the user to scenarios like py3cairo vs pycairo -- if the slackbuild calls for py3cairo, slackstack will alert the user that pycairo is installed and they can determine for themselves if the dependency is met.<br />
* Version numbers are now shown.  If slackstack finds the program it's building or a dependency already installed, it shows the version number of the installed program.<br />

__0.5.3__ slackstack has one important new feature -- now it searches the computer to see if the program being built or its dependencies are already installed.  In either case, it adds asterisks to the relevant entries in the installseq.txt file and shows [INSTALLED] on the screen output.<br />

### Release Notes for Slackgrab:<br />
__0.5.9__ whitespace cleanup<br />
__0.5.8__ urllib 403 error fix<br />
__0.5.7__ Refactor code, major cleanup and bug fixes<br />
__0.5.5__ Bug fix<br />
__0.5.3__ Bug fix, cleanup. Fixed an issued with Github tarballs having an incomplete name.<br />
__0.5.2__ Added --skip (or -s) flag to skip prompting for download location.<br />
__0.5.0__ slackgrab is a major revision.  The code is cleaner and handles *.info files in a more efficient manner.<br />
* Programs with multiple (unlimited) binaries are now supported.  This means things like the Nvidia driver are downloaded and verified correctly<br />
* The code now supports slackbuild *.info files where the tarball htmls are located in either the DOWNLOADS_x86_64 area or the DOWNLOADS area.  There is some variation among slackbuilds, so the program checks the x86 location first and moves to the other one if nothing is found.

### Near-term goals:<br />
* [PHASE2] combine utilities into one program
* [DONE] add support for local pip libraries
* [DONE] add support for multiple binary builds
* [DONE] Add user input to select directories<br />
* [DONE] Add slackgrab option to traverse multiple slackbuild directories and download tar files for each<br />
* [DONE] Search a local database for available slackbuilds (e.g., a local git clone of the slackbuilds repo)<br />
* [REPLACED] Search a remote database for available slackbuilds (e.g., slackbuilds.org)<br />

### Known bugs<br />
To handle incomplete tarball names that happen with Github, slackgrab does a sanity check on the tarball. However if a developer names their tarball something other than their program name -- say, foo-bar is the program name but the tarball is called bar.tar.gz -- slackgrab will misname it. This is very unusual, but I found one example of it so there may be others.

32-bit slackbuild support is fairly trivial to add for someone who needs it, but I personally have no plans to include it.<br />
