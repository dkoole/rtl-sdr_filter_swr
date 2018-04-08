import matplotlib.pyplot as plt
import subprocess
import csv

filter_baseline_file = "reference.csv"
filter_file = "filter.csv"
filter_output_file = "output.csv"
swr_baseline_file = "swr_baseline.csv"
swr_antenna_file = "swr_antenna.csv"
swr_output_file = "swr.csv"

if __name__ == "__main__":
	print "Script to measure filter characteristics and antenna VSWR with rtl-sdr dongle"
	measurement_name = raw_input("Name for measurement ")
	startFrequency = input("Enter start frequency in MegaHertz ")
	stopFrequency  = input("Enter stop frequenc in MegaHertz ")
	#measurementType = raw_input("Measurement type filter/swr ")
	measurementType = "swr"

	if measurementType.lower() == "filter" :
		print "Selected Filter characteristics measurement"
		reference_file = filter_baseline_file
		connected_file = filter_file
	else :
		print "Selected Antenna SWR measurement"
		reference_file = swr_baseline_file
		connected_file = swr_antenna_file

	# x = raw_input("Press Enter to start Baseline measurement ")

	# subprocess.call(["rtl_power", "-f", str(startFrequency) + "M:" + str(stopFrequency) + "M:1M", "-i", "10", "-1", "-g", "0", reference_file])
	# x  = raw_input("Press Enter to start next measurement")
	# subprocess.call(["rtl_power", "-f", str(startFrequency) + "M:" + str(stopFrequency) + "M:1M", "-i", "10", "-1", "-g", "0", connected_file])

	reference_power = []
	frequencies_start = []
	frequencies_stop = []
	connected_power = []
	# reference_list = []
	# attenuation = []

	with open(reference_file, 'rb') as ref_file:
		reader = csv.reader(ref_file, delimiter=",",quoting=csv.QUOTE_NONE)
		for row in reader:
			reference_power.append(row[6])
			frequencies_start.append(row[2])
			frequencies_stop.append(row[3])

	with open(connected_file, 'rb') as filt_file:
	 	reader = csv.reader(filt_file, delimiter=",",quoting=csv.QUOTE_NONE) 
		connected_power = [row[6] for row in reader]

	with open(swr_output_file, 'w') as csvfile:
		fieldnames = ['Frequency', '', 'Baseline', 'Antenna connected', 'Return Loss', 'Adjusted RL', 'SWR']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

		writer.writeheader()

		return_loss = []
		return_loss_corrected = []

		for i in xrange(len(reference_power)):
			return_loss.append(float(connected_power[i]) - float(reference_power[i]))
			return_loss_corrected.append(max(0.0001, return_loss[i]))
			base_calc = 10 * (return_loss_corrected[i] / 20)
			vswr = ((base_calc + 1) / (base_calc - 1))
			writer.writerow({'Frequency': frequencies_start[i], '': frequencies_stop[i], 'Baseline' : reference_power[i], 'Antenna connected' : connected_power[i], 'Return Loss' : return_loss[i], 'Adjusted RL' : return_loss_corrected[i], "SWR" : vswr})

	# with open(output_file, 'w') as csvfile:
	#     fieldnames = ['Frequency', '', 'Baseline dBm', 'Filter dBm', "Attenuation"]
	#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

	#     writer.writeheader()

	#     for i in xrange(len(reference)):
	#     	attenuation.append(float(filter_list[i]) - float(reference[i]))
	#     	writer.writerow({'Frequency': frequencies_start[i], '': frequencies_stop[i], 'Baseline dBm': reference[i], 'Filter dBm': filter_list[i], 'Attenuation' : float(filter_list[i]) - float(reference[i])})

	# plt.figure(1)
	# line_filter, = plt.plot(frequencies_start, filter_list, linewidth=3.0, label=measurement_name)
	# line_reference, = plt.plot(frequencies_start, reference, linewidth=3.0, label="Baseline")
	# plt.title(measurement_name, fontweight='bold')
	# plt.grid(True, linestyle='-')
	# plt.legend(handles=[line_reference, line_filter])
	# plt.ylabel('Power (dB)', fontweight='bold')
	# plt.xlabel('Frequency (Hz)', fontweight='bold')
	# plt.savefig("TestTest")

	# plt.figure(2)
	# attenuation_plot, = plt.plot(frequencies_start, attenuation, linewidth=3.0, label="Attenuation")
	# plt.title(measurement_name, fontweight='bold')
	# plt.grid(True, linestyle='-')
	# plt.legend(handles=[attenuation_plot])
	# plt.ylabel('Attenuation (dB)', fontweight='bold')
	# plt.xlabel('Frequency (Hz)', fontweight='bold')
	# plt.savefig("Attenuation")

	# plt.show()