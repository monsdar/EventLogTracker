# EventLogTracker
Just a small tool checking the Eventlog to see how long the computer was on (used for Timetracking)

* Export a csv-log from the EventLog: `TurnedOnTimesView.exe /scomma out.csv`
* Manually clean the log if needed
* Run `logger.py` with Python3 and check for `output.html` afterwards

# Licenses
* The tool TurnedOnTimesView.exe is distributed by NirSoft, find the [Download and License page here](http://www.nirsoft.net/utils/computer_turned_on_times.html).
* The Python-script is licensed under [MIT license](https://opensource.org/licenses/MIT)
