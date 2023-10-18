# CAN DataFrame Project

This project takes an input file containing CAN sensor data (not real data), parses it,
and then produces an output file as well as a summary file. The main python file is
can_parser.py. The syntax for the command is:

```sh
python can_parser.py -i sensor_input.txt -o sensor_output.txt -s sensor.log
```

A directory of test files is located in input_files. To run an example test, do the
following:

```sh
mkdir output_files
make output_files/Data_A_output.txt
```

To see a list of possible output files, simply run:

```sh
make available_targets
```

The requirements for the project can be found in the file "Week II Mini-Project.txt".
