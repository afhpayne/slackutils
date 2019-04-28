### Slackgrab

The goal of Slackgrab is to make working with slackbuilds easier.

At this stage, Slackgrab can:
(1) Download the 64-bit tar file to the currently open slackbuild directory.
(2) Verify the MD5sum for the downloaded file against the one in program_name.info

This is written in python and has no dependencies beyond the standard python library.

Near-term goals:
* Add user input to pick a slackbuild directory to read and download to
* Add user input to traverse multiple slackbuild directories and download tar files for each
* Maybe add 32-bit support
* Search a local database for available slackbuilds (e.g., a local git clone of the slackbuilds repo)
* Search a remote databse for available slackbuilds (e.g., slackbuilds.org)
* Download remote slackbuilds and check *.asc file agaist slackbuilds gpg key
