# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 17:30:21 2023

@author: kfranco 
Input: a txt file with RFU values in tabular format.
Output: a csv file with the following column headers:

plate_unique
plate_id
plate_well
rfu

The txt file from SpectraMax M3 generates an error with the function below.
To fix this I simply copied and pasted its content into a new txt file. 

The script below can works with txt files that have RFU data alone or OD620 
and RFU data. It was tested using both data types.

TO RUN, SIMPLY CHNAGE THE NAME OF THE .TXT FILE

"""





import csv
import os

def process_file(input_file):
    plate_unique = []
    plate_id = []
    plate_well = []
    rfu = []    
    with open(input_file, "r") as file:
        is_rfp = False
        for line in file:
            if "rfp" in line.lower():
                is_rfp = True
            else:
                pass
            
            if is_rfp:
                if "Plate:" in line:
                    plate_id.append (line.strip().split("\t")[1]) # get the second column from the tab-separated line
                elif "\t" in line:
                    data = line.split("\t")
                    if data [1][:4] == "Temp":
                        plate_well.append([x.strip() for x in data[2:98]]) 
                    else:
                        rfu.append([x.strip() for x in data[2:98]])
                elif "~End" in  line:
                    is_rfp = False
                else:
                    pass
            else:
                pass
            
        for i in range(len(plate_id)):
            plate_name = f"plate_{i}"
            plate_unique.append(plate_name)    
        output_file = os.path.splitext(input_file)[0] + ".csv"
        with open (output_file, "w", newline = "") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["plate_unique","plate_id", "plate_well", "rfu"])
            
            for i in range(len(plate_id)):
                for j in range(len(plate_well[i])):
                    writer.writerow([plate_unique[i], plate_id[i], plate_well[i][j], rfu[i][j]])
        print(f"Output written to {output_file}")


#change file name as needed  
process_file("soil_only.txt")




