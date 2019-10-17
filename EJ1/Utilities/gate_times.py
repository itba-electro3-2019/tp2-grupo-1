"""
This script reads a .csv file where the input and output data from a logic gate
has been saved by an oscilloscope, and returns the values of the input and output
time valeus, known as propagation and transition delays.

* This code assumes that the oscilloscope's channel 1 is the input and the channel 2 is the output.
* No validation is done, no time to think that much :(

Usage:
	python gate_times.py "data.csv"

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


def find_percent_time(time_values, channel_values, percent):
	RELATIVE_ERROR = 0.1

	min_value = min(channel_values)
	max_value = max(channel_values)
	target = min_value + (max_value - min_value) * percent

	found = None
	for channel_value in channel_values:
		if found is None:
			if abs(target - channel_value) < abs(target) * RELATIVE_ERROR:
				found = channel_value
		else:
			break

	time = time_values[numpy.where(channel_values == found)]
	return time


def get_transition_time(time_values, channel_values):
	time_10_percent = find_percent_time(time_values, channel_values, 0.1)
	time_90_percent = find_percent_time(time_values, channel_values, 0.9)
	
	time_10_percent = numpy.average(time_10_percent)
	time_90_percent = numpy.average(time_90_percent)
	
	return abs(time_90_percent - time_10_percent)


def get_propagation_time(time_values, input_values, output_values):
	input_time = find_percent_time(time_values, input_values, 0.5)
	output_time = find_percent_time(time_values, output_values, 0.5)
	
	input_time = numpy.average(input_time)
	output_time = numpy.average(output_time)
	
	return abs(input_time - output_time)


def gate_time(*args, **kwargs):
	# Constant settings of the file, TODO: Set this from the command-line arguments!
	START_INDEX = 1
	TIME_INDEX = 0
	INPUT_INDEX = 1
	OUTPUT_INDEX = 2
	
	# Read the file!
	raw_data = pandas.read_csv(args[0])
	
	# Start parsing values
	time_values = get_columns_since(raw_data, START_INDEX, TIME_INDEX)
	input_voltages = get_columns_since(raw_data, START_INDEX, INPUT_INDEX)
	output_voltages = get_columns_since(raw_data, START_INDEX, OUTPUT_INDEX)
	
	propagation = get_propagation_time(time_values, input_voltages, output_voltages)
	transition = get_transition_time(time_values, output_voltages)
	
	# Calculating the resulting values
	return {
		"propagation-time": propagation,
		"transition-time": transition
	}


if __name__ == "__main__":
	# Calling the main() function
	print(gate_time(sys.argv[1:][0]))
	sys.exit()
