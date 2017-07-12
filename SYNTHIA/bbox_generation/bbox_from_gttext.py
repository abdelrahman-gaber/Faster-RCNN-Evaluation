# this code reads the GT text files of SYNTHIA and generate bounding boxes around pedestrian class. 
# the output is in the form [col_min, row_min, col_max, row_max]
import numpy as np
import os
import math
import argparse
import cv2

def ReadGTTXTFile(filename):
	gt_seg = []
	f = open(filename)
	lines = f.read().splitlines()

	for l in lines:
		values = l.split(" ")
		gt_seg.append( [int(i) for i in values ])
	# NOTE: the output is array (720, 960) >> rows first then columns, not like image format	
	return np.asarray(gt_seg) 


def generate_bbox(seg_array):
	# seg_array is the original segmentation array read from the GTTXT files and converted to int
	person_label = np.argwhere(seg_array == 10) # pedestrian label == 10
	if not len(person_label): # if list is empty
		return -1
	
	row_min = np.argmin(person_label, axis = 0) [0]
	min_idx = person_label[row_min]
	
	# take sub array of original array, and find min and max borders of the person
	seg_array_sub = seg_array[ min_idx[0]  : -1  , min_idx[1] - 100 : min_idx[1] + 100 ]
		
	person_label2 = np.argwhere(seg_array_sub == 10)
	if not len(person_label2):
		return -1
	
	arg_min = np.argmin(person_label2, axis = 0)
	
	#min_row_sub = person_label2[arg_min[0]] # we already know it is in 0 location
	min_col_sub = person_label2[arg_min[1]]
	#print(min_row_sub, min_col_sub)
	
	arg_max = np.argmax(person_label2, axis = 0)
	max_row_sub = person_label2[arg_max[0]]
	max_col_sub = person_label2[arg_max[1]]
	#print(max_row_sub, max_col_sub)
	
	# annotation = [col_min, row_min, col_max, row_max ]
	margin = 5 # margin of n pixels in all sides of the rectangle
	annotation = [ min_col_sub[1]+min_idx[1]-100 - margin , min_idx[0]-margin , max_col_sub[1]+min_idx[1]-100+margin , max_row_sub[0]+min_idx[0]+margin ]

	return annotation

def Generate_bbox_rg(seg_array):
	print("Region Growing algorithm")
	# seg_array is the original segmentation array read from the GTTXT files and converted to int
	# person_label_idx = np.argwhere(seg_array == 10) # pedestrian label == 10
	annotations = []
	while(True):
		person_label_idx = np.argwhere(seg_array == 10) # pedestrian label == 10
		if not len(person_label_idx): # if list is empty
			break
			#return -1
	
		list_person_row = []
		list_person_col = []
		list_final_row = []
		list_final_col = []
		min_row = np.argmin(person_label_idx, axis = 0) [0]
		seed_idx = person_label_idx[min_row] # minimum index
		#print(seed_idx)

		#list_final_row.append(seed_idx[0])
		#list_final_col.append(seed_idx[1]) 
		list_person_row.append(seed_idx[0])
		list_person_col.append(seed_idx[1])
		
		while list_person_row: # while the list is not empty
			current_row = list_person_row[0]
			current_col = list_person_col[0]
			list_final_row.append(current_row)
			list_final_col.append(current_col)
			seg_array[current_row][current_col] = -1
			#print(list_person_row)
			del list_person_row[0]
			del list_person_col[0]

			# check neighbors of current pixels
			if seg_array[current_row-1][current_col-1] == 10 and not (current_row-1 in list_person_row) and not (current_col-1 in list_person_col):
				list_person_row.append(current_row-1)
				list_person_col.append(current_col-1)
				list_final_row.append(current_row-1)
				list_final_col.append(current_col-1)	

			if seg_array[current_row-1][current_col] == 10 and not (current_row-1 in list_person_row) and not (current_col in list_person_col):
				list_person_row.append(current_row-1)
				list_person_col.append(current_col)
				list_final_row.append(current_row-1)
				list_final_col.append(current_col)

			if seg_array[current_row-1][current_col+1] == 10 and not (current_row-1 in list_person_row) and not (current_col+1 in list_person_col):
				list_person_row.append(current_row-1)
				list_person_col.append(current_col+1)
				list_final_row.append(current_row-1)
				list_final_col.append(current_col+1)

			if seg_array[current_row][current_col-1] == 10 and not (current_row in list_person_row) and not (current_col-1 in list_person_col):
				list_person_row.append(current_row)
				list_person_col.append(current_col-1)
				list_final_row.append(current_row)
				list_final_col.append(current_col-1)

			if seg_array[current_row][current_col+1] == 10 and not (current_row in list_person_row) and not (current_col+1 in list_person_col):
				list_person_row.append(current_row)
				list_person_col.append(current_col+1)
				list_final_row.append(current_row)
				list_final_col.append(current_col+1)

			if seg_array[current_row+1][current_col-1] == 10 and not (current_row+1 in list_person_row) and not (current_col-1 in list_person_col):
				list_person_row.append(current_row+1)
				list_person_col.append(current_col-1)
				list_final_row.append(current_row+1)
				list_final_col.append(current_col-1)

			if seg_array[current_row+1][current_col] == 10 and not (current_row+1 in list_person_row) and not (current_col in list_person_col):
				list_person_row.append(current_row+1)
				list_person_col.append(current_col)
				list_final_row.append(current_row+1)
				list_final_col.append(current_col)

			if seg_array[current_row+1][current_col+1] == 10 and not (current_row+1 in list_person_row) and not (current_col+1 in list_person_col):
				list_person_row.append(current_row+1)
				list_person_col.append(current_col+1)
				list_final_row.append(current_row+1)
				list_final_col.append(current_col+1)


		# check list_final_* to find min-max row and col
		min_row = np.min(list_final_row)
		min_col = np.min(list_final_col)
		max_row = np.max(list_final_row)
		max_col = np.max(list_final_col)
		
		if (max_col - min_col > 30) or (max_row - min_row > 30):
			margin = 2	
			annotations.append([min_col-margin, min_row-margin, max_col+margin,  max_row+margin])
			print(annotations)

	return annotations	

if __name__ == "__main__":
	#file_name = "/data/stars/user/aabubakr/pd_datasets/datasets/SYNTHIA/GTTXT/ap_000_01-11-2015_19-20-57_000001_1_Rand_6.txt"
	#img_name = "/data/stars/user/aabubakr/pd_datasets/datasets/SYNTHIA/GT/ap_000_01-11-2015_19-20-57_000001_1_Rand_6.png"
	#file_name = "/data/stars/user/aabubakr/pd_datasets/datasets/SYNTHIA/GTTXT/ap_000_02-11-2015_18-02-19_000141_2_Rand_7.txt"
	#img_name = "/data/stars/user/aabubakr/pd_datasets/datasets/SYNTHIA/GT/ap_000_02-11-2015_18-02-19_000141_2_Rand_7.png"

	#seg_array = ReadGTTXTFile(file_name)
	#annot = Generate_bbox_rg(seg_array)
	#print(annot)
	#img = cv2.imread(img_name)
	#for ann in annot:
		#img = cv2.imread(img_name)
		#cv2.rectangle(img, (ann[0], ann[1]) , (ann[2], ann[3]), (0, 255, 0) , 2)

	#cv2.imwrite("rg_res.png", img)
	
		
	parser = argparse.ArgumentParser()
	
	parser.add_argument('-GTTXT', help = 'Path to ground truth text files', required = True )
	parser.add_argument('-output', help = 'Full path to output results file', required = True )
	parser.add_argument('-images', help = 'Path to original RGB images', required = False, default = None)

	args = vars(parser.parse_args())

	if args['GTTXT'] is not None:
		gt_txt_path = args['GTTXT']
	if args['output'] is not None:
		output_path = args['output']
	if args['images'] is not None:
                images_path = args['images']

	for files in os.scandir(gt_txt_path):
		if files.is_file() and files.name.endswith('.txt'):
			file_name = os.path.join(gt_txt_path, files.name)
			seg_array = ReadGTTXTFile(file_name)
			annotation = Generate_bbox_rg(seg_array)
			print(file_name)
			img_name = os.path.join(images_path, os.path.splitext(files.name)[0] + ".png")
			im_path = os.path.join(output_path , 'visualization-images', os.path.splitext(files.name)[0] + ".png" )
			out_path = os.path.join(output_path , 'annotations',os.path.splitext(files.name)[0] + ".txt" )
			
			f = open(out_path, 'w')
			if annotation:
				for annot in annotation: 
					f.write(str(annot[0]) + " " + str(annot[1]) + " " + str(annot[2]) + " " + str(annot[3]) + "\n")
			f.close()
			
			if args['images'] is not None:
				img = cv2.imread(img_name)
				for annot in annotation:
					cv2.rectangle(img, (annot[0], annot[1]) , (annot[2], annot[3]), (0, 255, 0) , 2)
				cv2.imwrite(im_path, img)

