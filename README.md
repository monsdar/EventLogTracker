# EventLogTracker
Just a small tool checking the Eventlog to see how long the computer was on (used for Timetracking)

* Export a csv-log from the EventLog by running TurnedOnTimesView like the following: `TurnedOnTimesView.exe /scomma out.csv`
* Sometimes you need to manually clean up the log
* Afterwards run the `logger.py` with Python3 and check for the written `output.html`

# Licenses
* The tool TurnedOnTimesView.exe is distributed by NirSoft, find the [Download page here](http://www.nirsoft.net/utils/computer_turned_on_times.html).
* The Python-script is licensed under [MIT license](https://opensource.org/licenses/MIT)
