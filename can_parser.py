from data_frame_parser import DataFrameParser
from datetime import datetime
from argparse import ArgumentParser
from typing import TextIO
import fileinput
import sys

NO_OF_FIELDS = 5

# According this link, it is better to pass file objects rather than file names:
# https://softwareengineering.stackexchange.com/questions/262346/should-i-pass-in-filenames-to-be-opened-or-open-files
def parse_sensor_file(input_file: TextIO, output_file: TextIO, summary_file: TextIO):
    """
    Parses a OBD sensor file and outputs it to output_file, while also writing a summary to summary_file

    :param input_file: File-like object whose contents to parse input from
    :param output_file: File-like object to write parsed data to
    :param summary_file: File-like object to write summary to
    """
    line_length = NO_OF_FIELDS * 2 + NO_OF_FIELDS - 1
    dfp = DataFrameParser()
    for frame_num, line in enumerate(input_file):
        if len(line) < line_length:
            raise IndexError("Line must consist of five hexadecimal bytes, space separated, not long enough")

        fields = line[:line_length].split()

        if len(fields) < 5:
            raise IndexError("Number of bytes in line less than five")
         
        output_file.write(f"{frame_num + 1} - {datetime.now().strftime('%X')} - {dfp.parse_frame(*fields[:5])}\n")
        
    summary_file.write(dfp.summary())

def main():
    """
    function to be executed if Python script executed directly
    """

    parser = ArgumentParser(
        prog = "CanParser",
        description = "Parses an input file with CAN sensor data",
        epilog = """Sensor input data should consist of lines of five hexadecimal bytes
        separated by spaces, with the first byte specifiying the sensor type, the middle
        three bytes specifying the data, and the last byte specifying the error.
        """
    )

    parser.add_argument("-i", "--input", help = "Name of sensor input file (defaults to standard input)")
    parser.add_argument("-o", "--output", help = "Name of file to output to (defaults to standard output)")
    parser.add_argument("-s", "--summary", help = "Name of summary file (defaults to standard error)")

    args = parser.parse_args()
    with (open(args.input, "r") if args.input else fileinput.input) as input_file,\
        (open(args.output, "w") if args.output else sys.stdout) as output_file,\
        (open(args.summary, "w") if args.summary else sys.stderr) as summary_file:
        parse_sensor_file(input_file, output_file, summary_file)

if __name__ == "__main__":
    main()
