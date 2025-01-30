import os
import pandas as pd

file_names = [
    "CompactDetectionLog-CTCE7_65dB10cm60dB30cm60dB2m.wav.txt",
    "CompactDetectionLog-CTCELC2_10cmVol9_2.wav.txt",
    "CompactDetectionLog-CTCELCWG2_1_60dB2m.wav.txt",
    "CompactDetectionLog-CTCELCWG2_1_65dB10cm60dB30cm_mic1.wav.txt",
    "CompactDetectionLog-CTCELCWG2_1_lineIn_VOL50.wav.txt",
    "CompactDetectionLog-KantarCertificationMeters.wav.txt",
    "dzikie_dane.txt",
]

for i in range(len(file_names)):
    file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        file_names[i],
    )

    print()
    print(str(i + 1) + ". ", file_path)
    print()

    df = pd.read_csv(
        filepath_or_buffer=file_path,
        sep="\t",
        header=None,
    )
    # df.fillna(value=0.0, inplace=True)
    df.columns = ["begin", "end", "type", "id", "timestamp"]

    print(df)
    print()

    indices_of_sequences = []
    for i, x in enumerate(df["ID"]):
        if x == "00002C48":  # searching for the right ID
            indices_of_sequences.append(i)

    print(indices_of_sequences)
    print()

    starts = []
    for index, i in enumerate(indices_of_sequences):
        # if watermark in one line
        length = (
            df.loc[i, "end"] - df.loc[i, "start"]
        )  # checking the length of watermark
        if (
            length >= 1107
        ):  # how to tune it? As we discussed last week, the tool is not very precise at the end, so this is a value that fits to files from You,
            # but may not in general
            start = (
                df.loc[i, "start"] - 90 - df.loc[i, "TST"]
            )  # finding the start of the sequence
            starts.append(start)
        else:
            if index > 0:
                # if watermark in two lines
                if indices_of_sequences[index] - indices_of_sequences[index - 1] == 1:
                    length = df.loc[i, "end"] - df.loc[i - 1, "start"]
                    if length >= 1107:
                        start = df.loc[i - 1, "start"] - 90 - df.loc[i - 1, "TST"]
                        starts.append(start)
                    else:  # if watermark in three ore more lines
                        counter = index
                        while length < 1107:
                            length = (
                                df.loc[indices_of_sequences[counter], "end"]
                                - df.loc[i - 1, "start"]
                            )
                            counter += 1
                        start = df.loc[i - 1, "start"] - 90 - df.loc[i - 1, "TST"]
                        starts.append(start)
                        break  # not the solution, I need to jump out of loop and iterate above counter (maybe recursion?)

    print(starts)
    print()

    # idea based on TST - not working yet
    sequence = []
    sequences = []
    for index, i in enumerate(df["ID"]):
        if i == "00002C48":
            length = (
                df.loc[index, "end"] - df.loc[index, "start"]
            )  # checking the length of watermark
            if length >= 1107:
                sequence.append(index)
                sequences.append(sequence)
                sequence = []
            else:
                if df.loc[index + 1, "start"] - df.loc[index, "end"] < 100:
                    if df.loc[index, "TST"] < df.loc[index + 1, "TST"]:
                        length = df.loc[index + 1, "end"] - df.loc[index, "start"]
                        if length >= 1107:
                            sequence.append(index)
                            sequences.append(sequence)
                            sequence = []
                        else:  # if watermark in three ore more lines
                            counter = index
                            while length < 1107:
                                length = (
                                    df.loc[counter, "end"] - df.loc[index - 1, "start"]
                                )
                                counter += 1

    print(sequences)
    print()

# here is what I expect without subtraction of the offset, but I manualy checked, that it is necessery to substract it
# what i expect from CompactDetectionLog-CTCE7_65dB10cm60dB30cm60dB2m.wav.txt: [47, 1409, 2876] - ok
# what i expect from CompactDetectionLog-CTCELC2_10cmVol9_2.wav.txt: [67.7] - ok
# what i expect from CompactDetectionLog-CTCELCWG2_1_60dB2m.wav.txt: [30.95] - ok
# what i expect from CompactDetectionLog-CTCELCWG2_1_65dB10cm60dB30cm_mic1.wav.txt: [67.7, 1320] - for some reason twice the same number, must be corrected, but for now ok
# what i expect from CompactDetectionLog-CTCELCWG2_1_lineIn_VOL50.wav.txt: [1.85] - ok
# what i expect from CompactDetectionLog-KantarCertificationMeters.wav.txt: [0.11] - ok
# test on my crazy_file: [1320, 3368.18] - it does not work smoothely
