### Slackutils

The goal of Slackutils is to make working with slackbuilds easier.

There are two utilities so far:

#### Slackstack:<br />
Uses a local clone of the slackbuilds.org git repository. <br />
(1) Searches for a program in the local dirs<br />
(2) Copies the slackbuild to a 'build' directory<br />
(3) Scans the slackbuild for dependencies and copies those slackbuilds to the build directory<br />
(4) Recursively scans all dependecies for additional dependencies... and so on until every *needed* slackbuild has been copied to the build directory<br />
(5) Creates a text file to show the installation order of the slackbuilds

#### Slackgrab:  
(1) Downloads the 64-bit tar file to the currently open slackbuild directory<br />
(2) Announces dependencies for the slackbuild<br />
(3) Verifies the MD5sum for the downloaded file against the one in the *.info file

Everything is written in python 3.6 and has no dependencies beyond the standard python library.

Near-term goals:<br />
* Add user input to select directories<br />
* Add slackgrab option to traverse multiple slackbuild directories and download tar files for each<br />
* Maybe add 32-bit support<br />
* [DONE] Search a local database for available slackbuilds (e.g., a local git clone of the slackbuilds repo)<br />
* Search a remote databse for available slackbuilds (e.g., slackbuilds.org)<br />
* Download remote slackbuilds and check *.asc file agaist slackbuilds gpg key