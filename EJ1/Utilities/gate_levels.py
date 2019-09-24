"""
This script read a .csv file where the input and output data from a logic gate
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


def main(*args, **kwargs):
	# Constant settings of the file, TODO: Set this from the command-line arguments!
	START_INDEX = 1
	INPUT_INDEX = 1
	OUTPUT_INDEX = 2
	RELATIVE_ERROR = 0.1	
	SAME_MARGIN = 10
	MIN_FILTER = 200
	
	# Read the file!
	raw_data = pandas.read_csv(args[0])
	
	# Start parsing values
	input_voltages = get_columns_since(raw_data, START_INDEX, INPUT_INDEX)
	output_voltages = get_columns_since(raw_data, START_INDEX, OUTPUT_INDEX)
	input_diff = numpy.diff(input_voltages)
	output_diff = numpy.diff(output_voltages)
	diff = output_diff / input_diff
	
	# Searching all possible targets
	targets = [(index, diff_value) for index, diff_value in enumerate(diff) if -RELATIVE_ERROR < diff_value + 1 < RELATIVE_ERROR]
	print("{} targets found!".format(len(targets)))
	new_targets = [targets[0]]
	
	for target in targets:
		repeated = False
		
		for new_target in new_targets:
			if abs(target[0] - new_target[0]) <= SAME_MARGIN:
				repeated = True
				break
				
		if not repeated:
			new_targets.append(target)
		else:
			continue
			
	print("{} targets with no repetition".format(len(new_targets)))
	
	target_indexes = [new_target[0] for new_target in new_targets if new_target[0] >= MIN_FILTER]
		
	print("{} targets after filtering".format(len(target_indexes)))
	
	# Calculating the resulting values
	if len(target_indexes) == 2:
		min_index = min(target_indexes)
		max_index = max(target_indexes)
		print(
			"VOH: {} VOL: {} VIH: {} VIL: {}".format(
				output_voltages[min_index],
				output_voltages[max_index],
				input_voltages[max_index],
				input_voltages[min_index]
			)
		)
	else:
		print("Some error was detected... more than 2 targets have been found! :(")
	


if __name__ == "__main__":
	# Calling the main() function
	main(sys.argv[1:][0])
	sys.exit()
