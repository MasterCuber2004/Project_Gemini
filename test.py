import fio.load_ct_img as ct
import cv2
import os
from csv import DictReader
import re

file_counter = 0
file_names_list = list()
first_window_values = list()

with open('DL_info.csv', 'r') as read_obj:
	csv_reader = DictReader(read_obj)

	for row in csv_reader:
		values_for_range = row['DICOM_windows'].strip('][').split(',')
		low_window, high_window = values_for_range[0], values_for_range[1]
		windows_to_add = [low_window, high_window]
		first_window_values.append(windows_to_add)
		counter = 0
		file_name_to_add = ""		
		for i in range(0, len(row['File_name'])):
			if counter <= 11:
				file_name_to_add = file_name_to_add + row['File_name'][i]
				counter = counter + 1
			else:
				counter = counter + 1
		file_names_list.append(file_name_to_add)
		
	#Removing duplicates from file_names_list
	final_file_names = []
	final_window_values = []
	window_counter = 0
	for element in file_names_list:
		if element not in final_file_names:
			final_file_names.append(element)
			x_counter = 0
			for x in first_window_values[window_counter]:
				x = float(x)
				first_window_values[window_counter][x_counter] = x
				x_counter = x_counter + 1				
			final_window_values.append(first_window_values[window_counter])
		window_counter = window_counter + 1

def convert_images(folder_list, window_values):
	windowing_counter = 0

	for i in folder_list:
		current_index = "Images_png/" + i
		current_folder = os.listdir(current_index)
		for i in current_folder:
			imname = current_index + "/" + i
			slice_idx, slice_intv, do_clip, num_slice = 1, 2, False, 1
			im, mask = ct.load_multislice_img_16bit_png(imname, slice_idx, slice_intv, do_clip, num_slice)
			win = window_values[windowing_counter] # obtained from DL_info.csv
			windowing_counter = windowing_counter + 1
			m = ct.windowing(im, win)
			cv2.imwrite(imname, im)

convert_images(final_file_names, final_window_values)




