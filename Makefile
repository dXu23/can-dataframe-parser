.POSIX:
.SUFFIXES:

output_files/output_data_sample.txt: input_files/input_data_sample.txt
	python can_parser.py -i $< -o $@ -s output_files/output_sample.log

output_files/Data_A_output.txt: input_files/Data_A.txt
	python can_parser.py -i $< -o $@ -s output_files/Data_A.log

output_files/Data_B_output.txt: input_files/Data_B.txt
	python can_parser.py -i $< -o $@ -s output_files/Data_B.log

output_files/Data_C_output.txt: input_files/Data_C.txt
	python can_parser.py -i $< -o $@ -s output_files/Data_C.log

output_files/LData_A_output.txt: input_files/LData_A.txt
	python can_parser.py -i $< -o $@ -s output_files/LData_A.log

output_files/LData_B_output.txt: input_files/LData_B.txt
	python can_parser.py -i $< -o $@ -s output_files/LData_B.log

output_files/LData_C_output.txt: input_files/LData_C.txt
	python can_parser.py -i $< -o $@ -s output_files/LData_C.log

.PHONY: clean available_targets

available_targets:
	grep '^output_files' Makefile | cut -d: -f1

clean:
	rm output_files/*
