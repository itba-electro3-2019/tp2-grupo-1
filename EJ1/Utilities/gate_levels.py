	"""
This script reads a .csv file where the input and output data from a logic gate
has been saved by an oscilloscope, and returns the values of the input and output
voltage levels, known as VIH, VIL, VOH, VOL.

* This code assumes that the oscilloscope's channel 1 is the input and the channel 2 is the output.
* No validation is done, no time to think that much :(

Usage:
	python gate_levels.py "data.csv"

Requirements:
	+ pandas
	+ numpy
"""

# module imports
import pandas
import numpy
import sys


def get_columns_since(file, start_index, data_index):
	return numpy.array([abs(float(row[data_index])) for index, row in enumerate(file.values) if index >= start_index])


def gate_level(*args, **kwargs):
	# Constant settings of the file, TODO: Set this from the command-line arguments!
	START_INDEX = 1
	INPUT_INDEX = 1
	OUTPUT_INDEX = 2
	RELATIVE_ERROR = 0.1
	SAME_MARGIN = 5
	MIN_FILTER = 200
	MAX_FILTER = 900
	
	# Read the file!
	raw_data = pandas.read_csv(args[0])
	
	# Start parsing values
	input_voltages = get_columns_since(raw_data, START_INDEX, INPUT_INDEX)
	output_voltages = get_columns_since(raw_data, START_INDEX, OUTPUT_INDEX)
	input_diff = numpy.diff(input_voltages)
	output_diff = numpy.diff(output_voltages)
	
	input_values = [(voltage, diff) for voltage, diff in zip(input_voltages, input_diff)]
	output_values = [(voltage, diff) for voltage, diff in zip(output_voltages, output_diff)]
	
	targets = []
	for input, output in zip(input_values, output_values):
		if input[1] != 0:
			diff = output[1] / input[1]
			
			if -RELATIVE_ERROR < diff + 1 < RELATIVE_ERROR:
				targets.append((diff, input[0], output[0]))
		else:
			continue
	
	# Separate High and Low candidates
	low_targets = high_targets = []
	
	for target in targets:
		if target[2] < 2.5:
			low_targets.append(target)
		else:
			high_targets.append(target)
	
	# Choosing only one
	low_target = high_target = None
	for target in low_targets:
		if low_target is None:
			low_target = target
		else:
			if target[2] > low_target[2]:
				low_target = target
	
	for target in high_targets:
		if high_target is None:
			high_target = target
		else:
			if target[2] < high_target[2]:
				high_target = target
	
	print("Final values!")
	print("Differential: {} - Vi: {} - Vo: {}".format(high_target[0], high_target[1], high_target[2]))
	print("Differential: {} - Vi: {} - Vo: {}".format(low_target[0], low_target[1], low_target[2]))

if __name__ == "__main__":
	# Calling the main() function
	print(gate_level(sys.argv[1:][0]))
	sys.exit()
