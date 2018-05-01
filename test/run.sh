#!/bin/bash

# This file should run code with timeouts sequentially
# for each student in the directory $rundir
#-----------------------------

# Add matlab
# add matlab
# If you want to add matlab via script, you need to add
# "source /usr/share/debathena-bash-config/bashrc.d/01-debathena-shell-init"
# at the front of this script

# This is a magic script, I don't know everything it does.  But I modified
# it to not need matlab, which was basically replacing 
# "run.call_matlab.sh" references to "run.call_python.sh" --Austin Collins

# How long to wait before timeout in seconds
timeoutperiod=3600;

source test.inc

for dir in $outputdir $resultdir $rundir $logdir $lockdir
do
  if [ ! -d $dir ]; then
      mkdir -p $dir
  fi
done

runlogfile="$logdir/run.log"
# File for list of names and times
timefile="$resultdir/execution_time.txt"
# rm -f $runlogfile $timefile
function log_run {
  echo "$@" >> $runlogfile
}
function echolog_run {
  echo "$@"
  echo "$@" >> $runlogfile
}

unziplogfile="$logdir/unzip.log"
status="$logdir/status.txt"
# rm -f $unziplogfile $status
function log_unzip {
  echo "$@" >> $unziplogfile
}
function echolog_unzip {
  echo "$@"
  echo "$@" >> $unziplogfile
}

log_run "---------- LOG FILE FOR PROJECT CODE EXECUTION, RUN AT `date`-----"
log_unzip "---------- LOG FILE FOR UNZIP COMMANDS, RUN AT `date`-----"


ZIPFILES=`ls -1 $srcdir | grep -E -x "[^@]*@mit\.edu\.[0-9]+\.zip"`
NAMES=`echo "$ZIPFILES" | awk -F@ '{print $1;}' | sort -u`
log_unzip "---"$(echo "$NAMES" | wc -w )" submissions to process---"
log_unzip $NAMES

list_of_unexpected_files=`ls -1 $srcdir | grep -v -E -x "[^@]*@mit\.edu\.[0-9]+\.zip"`
if [ -n "$list_of_unexpected_files" ]; then
    log_unzip "---Unexpected Files---"
    log_unzip "$list_of_unexpected_files"
fi

num_names=$(echo $NAMES | wc -w )
i=0
for NAME in $NAMES
do
  i=$((i+1))
  echo "-------- $NAME ($i/$num_names) --------"
  STAGE="deduplicate"
  while [[ "deduplicate clean unzip execute checkafs collectoutput" =~ "$STAGE" ]]; do
    case $STAGE in
      deduplicate )
        if [[ -d "$outputdir/$NAME" ]]; then
          echo "Skipped"
          STAGE="skipped"
          continue
        fi
        if [[ -f "$lockdir/$NAME" ]]; then
          echo "Skipped - $NAME is locked"
          STAGE="skipped"
          continue
        fi
        touch "$lockdir/$NAME"
        STAGE="clean"
        ;;
      clean )
        echo "Cleaning..."
        ./clean.sh $NAME
        STAGE="unzip"
        ;;
      unzip )
        log_unzip "-------------"
        log_unzip "Extracting to directory $NAME"
        echo -n "Extracting to directory $NAME, "
        possible_zip_file_numbers=$(echo "$ZIPFILES" | grep -E -x "$NAME"@.* | awk -F@ '{print $2;}' | awk -F. '{print $3;}' | sort --numeric-sort -r )

        for cnumber in $possible_zip_file_numbers
        do
            #check if one of the earlier ones gave rise to the directory
            #didn't find the decode function, will try unzipping this instance.
            if [ ! -e "$rundir/$NAME/decode.py" ]; then
                unzip "$srcdir/${NAME}@mit.edu.$cnumber.zip" -d "$rundir/$NAME" 2>&1 >> $unziplogfile
            fi
        done

        #At the end of this check if exists directory, etc.
        if [ -e $rundir/"$NAME"/decode.py ]
        then
            echolog_unzip "Success!"
            # echo -e "$NAME""\t\t Yes">>$status
            STAGE="execute"
        else
            if [ -d $rundir/"$NAME" ]
            then
                echolog_unzip "Error! \"decode.py\" not found."
                echo "$NAME Error: \"decode.py\" not found">>$status
            else
                echolog_unzip "Error! No directory created."
                echo "$NAME Error: cannot extract zip file">>$status
            fi
            mkdir -p "$outputdir/$NAME"
            STAGE="error"
            continue
        fi
        ;;
      execute )
        log_run "-----------"
        now=$(date +"%T")

        #Check if the file MCMCdecode.py exists
        if [ ! -e "$rundir/$NAME/decode.py" ];
        then
            # This branch should not be able to reach
            log_run "No file decode.m found in $NAME!"
            timeforexec=0
            STAGE="error"
            continue
        fi

        log_run "File found. "
        echolog_run "Executing submission from $NAME, started at $now"

        # Excellent. Run the command
        # /usr/bin/time -f 'real %e' -o .temp_time_output ./run.timeout.sh $timeoutperiod ./run.call_matlab.sh $NAME
        #/usr/bin/time -f 'real %e' -o $logdir/.temp_${NAME}_time_output timeout -k 10 $timeoutperiod ./run.call_matlab.sh $NAME
        /usr/bin/time -f 'real %e' -o $logdir/.temp_${NAME}_time_output timeout -k 10 $timeoutperiod ./run.call_python.sh $NAME
        sleep 1
        filereaderr=$(cat $logdir/.temp_${NAME}_time_output 2>&1)
        if [[ "$filereaderr" =~ "No such file or directory" ]] || [[ "$filereaderr" =~ "Connection timed out" ]]; then
            #statements
            echo "Unexpected error: $filereaderr"
            echo "fs checkservers: `fs checkservers`"
            # sleep 300
            # STAGE="clean"
            # continue
            exit
        fi
        timeforexec=$(cat $logdir/.temp_${NAME}_time_output | grep real | cut -f 2 -d ' ')
        rm -f $logdir/.temp_${NAME}_time_output

        # Echo to runlogfile and timefile
        log_run "Time for execution: "$timeforexec
        STAGE="checkafs"
        ;;
      checkafs )
        if [[ -n `aklog 2>&1` ]];
        then
            echo "your afs session is timeout, please login again"
            read -rsp $'(Press any key to continue...)\n' -n1
            until [[ -z `aklog 2>&1` ]]; do
                kinit
            done
            sleep 1
            STAGE="clean"
            continue
        fi
        STAGE="collectoutput"
        ;;
      collectoutput )
        echo "Collecting outputs of $NAME"

        echo "$NAME Finished in ${timeforexec}s" >> $status
        echo "$NAME $timeforexec">>$timefile

        # Copy the output files to $outputdir
        mkdir -p "$outputdir/$NAME"
        cp "$rundir/$NAME"/output* "$outputdir/$NAME" 2>&1 >> $runlogfile

        rm -f "$lockdir/$NAME"

        STAGE="finished"
        ;;
    esac
  done
done
