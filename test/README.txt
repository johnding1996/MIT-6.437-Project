If you have any suggestions for improvements, email dove@mit.edu or dgsong@mit.edu.


To run this test, you must be logged in to an athena machine, e.g. in-person at a cluster or 
remotely via athena.dialup.  When on athena, in a terminal window:

1. zip your code all in a zip file with the name: <your MIT id>@mit.edu.1.zip, i.e. run

    zip <your MIT id>@mit.edu.1.zip *

when in the directory containing your code (which should contain decode.py that has
a decode function as specified in the project description).  Put this zip file
in the "zip_files" directory.
2. run ./clean.sh
3. run ./run.sh
4. Look in outputs/<your MIT id>, there should be text files with the output from your program.
5. When running it again, always run ./clean.sh before running ./run.sh.
