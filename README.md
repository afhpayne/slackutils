### Slackutils

The goal of Slackutils is to make working with slackbuilds easier.

#### Release Notes:<br />
0.5.3 slackstack has one important new feature -- now it searchs the computer to see if the program being built is already installed.  If the program or any of its dependencies are installed, it adds asterisks to the relevant entries in the installseq.txt file and shows [INSTALLED] on the screen output. 

0.5.0 slackgrab is a major revision.  The code is cleaner and handles *.info files in a more efficient manner.<br />
** Programs with multiple (unlimited) binaries are now supported.  This means things like the Nvidia driver are downloaded and verified correctly<br />
** The code now supports slackbuild *.info files where the tarball htmls are located in eithe DOWNLOADS_x86_64 area or the DOWNLOADS area.  There is some variation among slackbuilds, so the program checks the x86 location first and moves to the other one if nothing is found.


#### There are two utilities -- slackstack and slackgrab

#### Slackstack:<br />
Uses a local clone of the slackbuilds.org git repository <br />
1. Searches for a program in the local clone or user folder<br />
2. Copies the slackbuild to a 'build' directory --> default = ~/slackstack/[program_name]-tree<br />
3. Scans the slackbuild for dependencies and copies *those* slackbuilds to the build directory<br />
4. Recursively scans all dependecies for additional dependencies... and so on until every *needed* slackbuild has been copied to the build directory<br />
5. Creates a text file to show the installation order of the slackbuilds
6. Sets the *.SlackBuild file permissions in each folder to executable

#### Slackgrab:  
1. Asks if the user wants to iterate through all folders in build directory (see above) to identify needed tar files<br />
2. Downloads the 64-bit tar files to the matching slackbuild directory<br />
3. Verifies the MD5sum for the downloaded files against the one in the respective *.info files
4. Allows the user to use the default build location (/home/user/slackstack) or to choose another

Everything is written in python 3.8 and has no dependencies beyond the standard python library.

Near-term goals:<br />
* [DONE] add support for multiple binary builds
* combine utilities into one program
* [DONE] Add user input to select directories<br />
* [DONE] Add slackgrab option to traverse multiple slackbuild directories and download tar files for each<br />
* [PHASE1] Maybe add 32-bit support<br />
* [DONE] Search a local database for available slackbuilds (e.g., a local git clone of the slackbuilds repo)<br />
* Search a remote databse for available slackbuilds (e.g., slackbuilds.org)<br />

