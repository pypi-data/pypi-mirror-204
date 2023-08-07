# Serial Data Logger

A simple python script that logs the input received from a serial (USB) input to an SQLite database along with logging the time stamp (in the format YYMMDDHHMMSS) of the received message.
Serial data logger expects the serial inputs to be comma separated.

## Usage

Here's an example using a Finometer pressure sensor.

```python
import logging
import serialdatalog as sdl

logging.basicConfig(level=logging.INFO)
# table_dict is formed of key : value pairs consisting of:
#   sql_header : sql_data_type
# If the number of headers is different to that read from the serial input then the input is not
# logged.
table_dict = {
    "Elapsed_Time" : "REAL",
    "Finger_Pressure" : "REAL",
    "Height" : "REAL",
    "Arm_Pressure" : "REAL",
    "Finger_Plethysmogram" : "REAL",
}
sdl.logger(
    table_dict,
    source="/dev/ttyACM0",
    dest="datalog.sqlite3",
    encoding='utf-8',
    timeout=10
)
```
