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
    "test-1.txt",
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
    df.columns = ["begin", "end", "type", "id", "timestamp"]

    print(df)
    print()

    flag = False
    begin_timestamps = []
    ZERO = numpy.float64(0.0)
    WATERMARK_SEQUENCE_LENGTH = numpy.float64(1107.0)
    WHITE_NOISE_SEQUENCE_LENGTH = numpy.float64(90.0)

    for j in range(len(df)):
        if not flag:
            if df.iloc[j]["id"] == "00002C48":
                begin = df.iloc[j]["begin"]
                timestamp = df.iloc[j]["timestamp"]
                begin_timestamp = (
                    begin
                    - WHITE_NOISE_SEQUENCE_LENGTH
                    - (ZERO if numpy.isnan(timestamp) else timestamp)
                )
                duration = df.iloc[j]["end"] - begin
                if duration >= WATERMARK_SEQUENCE_LENGTH:  # watermark in a single line
                    begin_timestamps.append(begin_timestamp)
                else:  # watermark in more than just one line
                    flag = True
        elif df.iloc[j]["id"] == "00002C48":  # watermark in more than just one line
            duration = df.iloc[j]["end"] - begin
            if duration >= WATERMARK_SEQUENCE_LENGTH:
                # end of watermark in more than just one line
                flag = False
                begin_timestamps.append(begin_timestamp)
        elif df.iloc[j]["id"] == "0000912A":
            # end of watermark in more than just one line
            flag = False
            begin_timestamps.append(begin_timestamp)

    print(begin_timestamps)
    print()
    print()

# here is what I expect without subtraction of the offset, but I manualy checked, that it is necessery to substract it
# what i expect from CompactDetectionLog-CTCE7_65dB10cm60dB30cm60dB2m.wav.txt: [47, 1409, 2876] - ok
# what i expect from CompactDetectionLog-CTCELC2_10cmVol9_2.wav.txt: [67.7] - ok
# what i expect from CompactDetectionLog-CTCELCWG2_1_60dB2m.wav.txt: [30.95] - ok
# what i expect from CompactDetectionLog-CTCELCWG2_1_65dB10cm60dB30cm_mic1.wav.txt: [67.7, 1320] - for some reason twice the same number, must be corrected, but for now ok
# what i expect from CompactDetectionLog-CTCELCWG2_1_lineIn_VOL50.wav.txt: [1.85] - ok
# what i expect from CompactDetectionLog-KantarCertificationMeters.wav.txt: [0.11] - ok
# test on my crazy_file: [1320, 3368.18] - it does not work smoothely
