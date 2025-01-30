import os
import numpy
import pandas

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

    if not os.path.isfile(file_path):
        print(file_path, "file likely does not exist")
        continue

    print(file_path)
    print()

    df = pandas.read_csv(
        filepath_or_buffer=file_path,
        sep="\t",
        header=None,
    )
    df.fillna(value=0.0, inplace=True)
    df.columns = ["begin", "end", "type", "id", "timestamp"]
    df: pandas.DataFrame = df.loc[df["id"] == "00002C48"]

    print(df)
    print()

    flag = False
    begin_timestamps = []
    TOTAL_SEQUENCE_LENGTH = 1107.0

    for j in range(len(df)):
        if not flag:
            begin = df.iloc[j]["begin"]
            timestamp = df.iloc[j]["timestamp"]
            duration = df.iloc[j]["end"] - begin
            if duration >= TOTAL_SEQUENCE_LENGTH:
                # watermark in a single line
                begin_timestamp = begin - 90.0 - timestamp
                if begin_timestamp < 0.0:
                    begin_timestamp = numpy.float64(0.0)
                begin_timestamps.append(begin_timestamp)
            else:
                # watermark in more than just one line
                flag = True
        else:
            # watermark in more than just one line
            duration += df.iloc[j]["end"] - begin
            if duration >= TOTAL_SEQUENCE_LENGTH:
                begin_timestamp = begin - 90.0 - timestamp
                if begin_timestamp < 0.0:
                    begin_timestamp = numpy.float64(0.0)
                begin_timestamps.append(begin_timestamp)
                flag = False

    print(begin_timestamps)
    print()

# here is what I expect without subtraction of the offset, but I manualy checked, that it is necessery to substract it
# what i expect from CompactDetectionLog-CTCE7_65dB10cm60dB30cm60dB2m.wav.txt: [47, 1409, 2876] - ok
# what i expect from CompactDetectionLog-CTCELC2_10cmVol9_2.wav.txt: [67.7] - ok
# what i expect from CompactDetectionLog-CTCELCWG2_1_60dB2m.wav.txt: [30.95] - ok
# what i expect from CompactDetectionLog-CTCELCWG2_1_65dB10cm60dB30cm_mic1.wav.txt: [67.7, 1320] - for some reason twice the same number, must be corrected, but for now ok
# what i expect from CompactDetectionLog-CTCELCWG2_1_lineIn_VOL50.wav.txt: [1.85] - ok
# what i expect from CompactDetectionLog-KantarCertificationMeters.wav.txt: [0.11] - ok
# test on my crazy_file: [1320, 3368.18] - it does not work smoothely
