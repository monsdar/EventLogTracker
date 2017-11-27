
from datetime import datetime
from datetime import timedelta

WORK_SECS = 8*60*60
PAUSE_SECS = 30 * 60
WORKDAY_SECS = WORK_SECS + PAUSE_SECS
WEEKDAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

class Record(object):
    def __init__(self):
        self.timestamp = None #datetime
        self.duration_sec = None #timedelta
    def __eq__(self, other):
        if isinstance(other, Record): #check type Record
            return (self.timestamp == other.timestamp)
        elif isinstance(other, datetime): #check type datetime)
            return (self.timestamp == other)
        else:
            return False
    def __lt__(self, other):
        return self.timestamp < other.timestamp
    def __hash__(self):
        return hash(self.timestamp)
        
class TableRow(object):
    def __init__(self):
        self.date = None
        self.duration = None
        self.color = 'style="background-color:grey"'
        self.plusminus = 0

#read file
lines = []
with open('log.csv') as f:
    lines = f.readlines()

#get records
records = []
for line in lines[1:]:
    fields = line.split(',')
    
    newRecord = Record()
    dateObj = datetime.strptime(fields[0].split(' ')[0], '%d.%m.%Y')
    newRecord.timestamp = dateObj
    
    try:
        datetimeObj = datetime.strptime(fields[3], '%H:%M:%S')
        newRecord.duration_sec = timedelta(hours=datetimeObj.hour, minutes=datetimeObj.minute, seconds=datetimeObj.second)
    except ValueError:
        newRecord.duration_sec = timedelta(0)
    
    if newRecord in records:
        existingRecord = records[records.index(newRecord)]
        if(existingRecord.duration_sec != newRecord.duration_sec):
            existingRecord.duration_sec += newRecord.duration_sec
    else:
        records.append(newRecord)

#gather all the rows
records.sort()
firstDate = records[0].timestamp
lastDate = records[len(records)-1].timestamp
deltaBetweenRecords = lastDate - firstDate #timedelta

rows = []
for index in range(deltaBetweenRecords.days + 1):
    newRow = TableRow()
    currentDate = firstDate + timedelta(days=index)
    newRow.date = currentDate
    
    try:
        newRow.duration = records[records.index(currentDate)].duration_sec
    except ValueError:
        newRow.duration = timedelta(0)

    if(newRow.duration.total_seconds() >= WORKDAY_SECS) or (newRow.date.weekday() == 5 or newRow.date.weekday() == 6): #working on the weekend is always overtime:
        newRow.color = 'style="background-color:green"'
    elif(newRow.duration.total_seconds() <= WORKDAY_SECS and newRow.duration.total_seconds() > 0):
        newRow.color = 'style="background-color:red"'
    
    if(newRow.duration.total_seconds() > 0):
        newRow.plusminus = newRow.duration.total_seconds()
        if not(newRow.date.weekday() == 5 or newRow.date.weekday() == 6): #working on the weekend is always overtime
            newRow.plusminus -= WORKDAY_SECS
    rows.append(newRow)

#start writing the HTML output
with open('output.html', 'w') as htmlHandle:
    htmlHandle.write('''
                    <!DOCTYPE html>
                    <html>
                    <head>
                    <style>
                    table {
                        font-family: arial, sans-serif;
                        border-collapse: collapse;
                    }

                    td, th {
                        border: 1px solid #dddddd;
                        text-align: left;
                        padding: 8px;
                    }
                    </style>
                    </head>
                    <body>
                    ''')
    htmlHandle.write('<table>\n')
    htmlHandle.write('<th>Year</th><th>Month</th><th>Week</th><th>Date</th><th>Weekday</th><th>Duration</th><th>+/-</th><th>Week</th><th>Total</th>\n')
    weekCounter = 0
    totalCounter = 0
    for row in rows:
        htmlHandle.write('<tr>\n')
        if(row.date.day == 1 and row.date.month == 1):
            htmlHandle.write('<td>' + row.date.year + '</td>\n')
        else:
            htmlHandle.write('<td></td>\n')
            
        if(row.date.day == 1):
            htmlHandle.write('<td>' + MONTHS[row.date.month-1] + '</td>\n')
        else:
            htmlHandle.write('<td></td>\n')
            
        if(row.date.weekday() == 0):
            htmlHandle.write('<td>Week ' + str(row.date.isocalendar()[1]) + '</td>\n')
        else:
            htmlHandle.write('<td></td>\n')
            
        htmlHandle.write('<td>' + row.date.strftime('%d-%m-%y') + '</td>\n')
        htmlHandle.write('<td>' + WEEKDAYS[row.date.weekday()] + '</td>\n')
        htmlHandle.write('<td ' + row.color + '>' + str(row.duration) + '</td>\n')
        htmlHandle.write('<td ' + row.color + '>' + str(timedelta(seconds=abs(row.plusminus))) + '</td>\n')
        
        weekCounter += row.plusminus
        if(row.date.weekday() == 6):
            color = 'style="background-color:red"'
            if(weekCounter > 0):
                color = 'style="background-color:green"'
            htmlHandle.write('<td ' + color + '>' + str(timedelta(seconds=abs(weekCounter))) + '</td>\n')
            weekCounter = 0.0
        else:
            htmlHandle.write('<td></td>\n')
            
        totalCounter += row.plusminus
        color = 'style="background-color:red"'
        if(totalCounter > 0):
            color = 'style="background-color:green"'
        htmlHandle.write('<td ' + color + '>' + str(timedelta(seconds=abs(totalCounter))) + '</td>\n')
        
        htmlHandle.write('</tr>\n')
    htmlHandle.write('</table>\n')
    htmlHandle.write('</body>\n')
    htmlHandle.write('</html>\n')

print("Total records: " + str(len(records)))