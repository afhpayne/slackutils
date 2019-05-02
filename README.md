### Slackutils

The goal of Slackutils is to make working with slackbuilds easier.

There are two utilities so far:

#### Slackstack:<br />
Uses a local clone of the slackbuilds.org git repository. <br />
1. Searches for a program in the local clone or user folder<br />
2. Copies the slackbuild to a 'build' directory [default = ~/Desktop/build]<br />
3. Scans the slackbuild for dependencies and copies *those* slackbuilds to the build directory<br />
4. Recursively scans all dependecies for additional dependencies... and so on until every *needed* slackbuild has been copied to the build directory<br />
5. Creates a text file to show the installation order of the slackbuilds
6. Sets the *.SlackBuild file permissions in each folder to executable

#### Slackgrab:  
1. Asks if the user wants to iterate through all folders in build directory (see above) to identify needed tar files<br />
2. Downloads the 64-bit tar files to the matching slackbuild directory<br />
3. Announces the dependencies for the slackbuild<br />
4. Verifies the MD5sum for the downloaded files against the one in the respective *.info files
5. The user can also choose to entry a particular slackbuild folder and download/verify *only* that tar file

Everything is written in python 3.6 and has no dependencies beyond the standard python library.

Near-term goals:<br />
* [DONE] Add user input to select directories<br />
* [DONE] Add slackgrab option to traverse multiple slackbuild directories and download tar files for each<br />
* Maybe add 32-bit support<br />
* [DONE] Search a local database for available slackbuilds (e.g., a local git clone of the slackbuilds repo)<br />
* Search a remote databse for available slackbuilds (e.g., slackbuilds.org)<br />
* Download remote slackbuilds and check *.asc file agaist slackbuilds gpg key