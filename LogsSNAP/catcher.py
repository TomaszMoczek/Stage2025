import numpy as np
import os
import pandas as pd


file_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "dzikie_dane.txt",
)

print(file_path)
with open(file_path, "r") as file_in:
    lines = []
    for line in file_in:
        lines.append(line)


data = pd.read_csv(
    file_path,
    nrows=len(lines),  # Number of rows of file to read
    header=None,  # Row number to use as column names
    sep="\t",  # Delimiter to use
    comment="#",  # Character to split comments
    na_values=[""],
)  # String to recognize as NA/NaN

df = pd.DataFrame(data)

df.columns = ["start", "end", "type", "ID", "TST"]

indices_of_sequences = []
for i, x in enumerate(df["ID"]):
    if x == "00002C48": #searching for the right ID
        indices_of_sequences.append(i)
print(indices_of_sequences)

starts = []
ios = indices_of_sequences.copy()
for index, i in enumerate(indices_of_sequences):
    #if watermark in one line
    length = df.loc[i, 'end'] - df.loc[i, 'start'] #checking the length of watermark
    if length >= 1107: #how to tune it? As we discussed last week, the tool is not very precise at the end, so this is a value that fits to files from You, 
        #but may not in general
        start = df.loc[i, 'start'] - 90 - df.loc[i, 'TST'] #finding the start of the sequence
        starts.append(start)
        ios.remove(i)
    else:
        if index > 0:
            #if watermark in two lines
            if indices_of_sequences[index] - indices_of_sequences[index - 1] == 1:
                length = df.loc[i, 'end'] - df.loc[i - 1, 'start']
                if length >= 1107:
                    start = df.loc[i - 1, 'start'] - 90 - df.loc[i-1, 'TST']
                    starts.append(start)
                    ios.remove(i - 1, i)
                else: #if watermark in three ore more lines
                    counter = index
                    while length < 1107:
                        length = df.loc[indices_of_sequences[counter], 'end'] - df.loc[i - 1, 'start']
                        counter += 1
                    start = df.loc[i - 1, 'start'] - 90 - df.loc[i-1, 'TST']
                    starts.append(start)
                    ios = np.delete(ios, list(range(index - 1, counter)), axis = 0)
                    break #not the solution, I need to jump out of loop and iterate above counter (maybe recursion?)

#ios = indices_of_sequences.copy()
#idea based on TST - not working yet
sequences = []
sequence = []
for index, i in enumerate(df['ID']):
    if x == "00002C48":
        length = df.loc[i, 'end'] - df.loc[i, 'start'] #checking the length of watermark
        if length >= 1107:
            sequence.append(i)
            sequences.append(sequence)
            sequence = []
        else:
            if df.loc[index + 1, 'start'] - df.loc[index, 'end'] < 100:
                if df.loc[index, 'TST'] < df.loc[index + 1, 'TST'] :
                
                    length = df.loc[i, 'end'] - df.loc[i - 1, 'start']
                    if length >= 1107:
                        sequence.append(i)
                        sequences.append(sequence)
                        sequence = []
                    else: #if watermark in three ore more lines
                        counter = index
                        while length < 1107:
                            length = df.loc[indices_of_sequences[counter], 'end'] - df.loc[i - 1, 'start']
                            counter += 1
                        

                        
print(ios)                    
print(len(ios))
starts = list(dict.fromkeys(starts))
print(starts)

    
#here is what I expect without subtraction of the offset, but I manualy checked, that it is necessery to substract it
#what i expect from CompactDetectionLog-CTCE7_65dB10cm60dB30cm60dB2m.wav.txt: [47, 1409, 2876] - ok
#what i expect from CompactDetectionLog-CTCELC2_10cmVol9_2.wav.txt: [67.7] - ok
#what i expect from CompactDetectionLog-CTCELCWG2_1_60dB2m.wav.txt: [30.95] - ok
#what i expect from CompactDetectionLog-CTCELCWG2_1_65dB10cm60dB30cm_mic1.wav.txt: [67.7, 1320] - for some reason twice the same number, must be corrected, but for now ok
#what i expect from CompactDetectionLog-CTCELCWG2_1_lineIn_VOL50.wav.txt: [1.85] - ok
#what i expect from CompactDetectionLog-KantarCertificationMeters.wav.txt: [0.11] - ok
#test on my crazy_file: [1320, 3368.18] - it does not work smoothely