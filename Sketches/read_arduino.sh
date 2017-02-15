#!/bin/bash
# Data Slam Script v0.1
# User define Function (UDF)
LogLine(){
  echo -E "`date +%s`,${line}"
 sqlite3 arduino.db3 "insert into arduino_data(time_stamp,millis,di2,di3,di4,di5,di6,di7,di8,di9,di10,di11,di12,ai1,ai2,ai3,ai4,ai5,ai6) values (`date +%s`,${line})"
} 
### Main script stars here ###
# Store file name
FILE=""
 
# Make sure we get file name as command line argument
# Else read it from standard input device
stty -F /dev/ttyACM0 cs8 115200 ignbrk -brkint -icrnl -imaxbel -opost -onlcr -isig -icanon -iexten -echo -echoe -echok -echoctl -echoke noflsh -ixon -crtscts
if [ "$1" == "" ]; then
   FILE="/dev/ttyACM0"
else
   FILE="$1"
   # make sure file (serial device) exist and is readable
   if [ ! -f $FILE ]; then
  	echo "$FILE : does not exists"
  	exit 1
   elif [ ! -r $FILE ]; then
  	echo "$FILE: can not read"
  	exit 2
   fi
fi
# Create Database if it does not exist
 
if [ ! -f "arduino.db3" ]; then
  	echo "Creating database"
        sqlite3 arduino.db3 "CREATE TABLE arduino_data (time_stamp integer ,millis integer, di2 integer, di3 integer, di4 integer, di5 integer, di6 integer,
                          di7 integer, di8 integer, di9 integer, di10 integer, di11 integer, di12 integer,
                          ai1 integer, ai2 integer, ai3 integer, ai4 integer, ai5 integer, ai6 integer);"
fi
exec 3<&0
exec 0<"$FILE"
while true
do
 
	# use $line variable to process line in processLine() function
	while read -r line
        do
              LogLine $line
        done
       usleep 50000 # This delay can be changed to match the delay of the Arduino
done
exec 0<&3
exit 0