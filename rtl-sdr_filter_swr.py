import matplotlib.pyplot as plt
import subprocess
import csv

reference_file = "reference.csv"
filter_file = "filter.csv"
output_file = "output.csv"

if __name__ == "__main__":
	print "Script to measure Filters and VSWR with rtl-sdr dongle"
	measurement_name = raw_input("Name for measurement")
	startFrequency = input("Enter start frequency in MegaHertz ")
	stopFrequency  = input("Enter stop frequenc in MegaHertz ")

	x = raw_input("Press Enter to start Baseline measurement ")

	subprocess.call(["rtl_power", "-f", str(startFrequency) + "M:" + str(stopFrequency) + "M:1M", "-i", "10", "-1", "-g", "0", reference_file])
	x  = raw_input("Press Enter to start next measurement")
	subprocess.call(["rtl_power", "-f", str(startFrequency) + "M:" + str(stopFrequency) + "M:1M", "-i", "10", "-1", "-g", "0", filter_file])

	reference = []
	frequencies_start = []
	frequencies_stop = []
	filter_list = []
	reference_list = []
	attenuation = []

	with open(reference_file, 'rb') as ref_file:
		reader = csv.reader(ref_file, delimiter=",",quoting=csv.QUOTE_NONE)
		for row in reader:
			reference.append(row[6])
			frequencies_start.append(row[2])
			frequencies_stop.append(row[3])

	with open(filter_file, 'rb') as filt_file:
	 	reader = csv.reader(filt_file, delimiter=",",quoting=csv.QUOTE_NONE) 
		filter_list = [row[6] for row in reader]

	with open(output_file, 'w') as csvfile:
	    fieldnames = ['Frequency', '', 'Baseline dBm', 'Filter dBm', "Attenuation"]
	    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

	    writer.writeheader()

	    for i in xrange(len(reference)):
	    	attenuation.append(float(filter_list[i]) - float(reference[i]))
	    	writer.writerow({'Frequency': frequencies_start[i], '': frequencies_stop[i], 'Baseline dBm': reference[i], 'Filter dBm': filter_list[i], 'Attenuation' : float(filter_list[i]) - float(reference[i])})

	plt.figure(1)
	line_filter, = plt.plot(frequencies_start, filter_list, linewidth=3.0, label=measurement_name)
	line_reference, = plt.plot(frequencies_start, reference, linewidth=3.0, label="Baseline")
	plt.title(measurement_name, fontweight='bold')
	plt.grid(True, linestyle='-')
	plt.legend(handles=[line_reference, line_filter])
	plt.ylabel('Power (dB)', fontweight='bold')
	plt.xlabel('Frequency (Hz)', fontweight='bold')
	plt.savefig("TestTest")

	plt.figure(2)
	attenuation_plot, = plt.plot(frequencies_start, attenuation, linewidth=3.0, label="Attenuation")
	plt.title(measurement_name, fontweight='bold')
	plt.grid(True, linestyle='-')
	plt.legend(handles=[attenuation_plot])
	plt.ylabel('Attenuation (dB)', fontweight='bold')
	plt.xlabel('Frequency (Hz)', fontweight='bold')
	plt.savefig("Attenuation")

	plt.show()