This is a python library to parse a cron expression .


Features:
1) Parses Hour String in expression .
Suported: */,- and [0-9]

2) Parses Minute string in expression.
Suported: */,- and [0-9]

3) parses dayOfMonth
Suported: */,- and [0-9]

4) Month
Suported: */,-  and [0-9] and JAN-DEC

5) dayOfWeek
Suported: */,-  and [0,9] and SUN-MON

*	any value
,	value list separator
-	range of values
/	step values

How to use:
1) Download this code repo in directory (say ~/workspace)
2) Run command "python parseArgs.py minuteStr hourStr dayOfMonth month dayOfWeek command"

Usage: parseArgs.py [-h] minuteStr hourStr dayOfMonth month dayOfWeek command

Ex: python parseArgs.py 1,3 2 1-5 1 1 /user/command
Output:
Minutes: [1, 3]
Hours: [2]
daysOfMonth: [1, 2, 3, 4, 5]
Months: [1]
Day of week: [1]
Command:  /user/command



Dependencies:
1) Install
Linux/Mac-

pip install argparse
pip install unittest

