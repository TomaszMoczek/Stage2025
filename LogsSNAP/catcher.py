import os
import numpy
import pandas
import scipy
from matplotlib import pyplot

file_names = [
    "CompactDetectionLog-CTCE7_65dB10cm60dB30cm60dB2m.wav.txt",
    "CompactDetectionLog-CTCELC2_10cmVol9_2.wav.txt",
    "CompactDetectionLog-CTCELCWG2_1_60dB2m.wav.txt",
    "CompactDetectionLog-CTCELCWG2_1_65dB10cm60dB30cm_mic1.wav.txt",
    "CompactDetectionLog-CTCELCWG2_1_lineIn_VOL50.wav.txt",
    "CompactDetectionLog-KantarCertificationMeters.wav.txt",
    "CompactDetectionLog-CTCE7_10cmvol9_1.wav.txt",
    "CompactDetectionLog-CTCE7_10cmvol9_2.wav.txt",
    "CompactDetectionLog-CTCE7_30cm_1m_vol7.wav.txt",
    "CompactDetectionLog-CTCELC2_30cm_1m_vol7.wav.txt",
    "CompactDetectionLog-CTCELC2_GluedVol7.wav.txt",
    # "test-1.txt",
]


file_names_wav = [
    "../Captures/raw/CTCE7_65dB10cm60dB30cm60dB2m.wav",
    "../Captures/raw/CTCELC2_10cmVol9_2.wav",
    "../Captures/raw/CTCELCWG2_1_60dB2m.wav",
    "../Captures/raw/CTCELCWG2_1_65dB10cm60dB30cm_mic1.wav",
    "../Captures/raw/CTCELCWG2_1_lineIn_VOL50.wav",
    "../KantarCertificationMeters.wav",
    "../Captures/raw/CTCE7_10cmvol9_1.wav",
    "../Captures/raw/CTCE7_10cmvol9_2.wav",
    "../Captures/raw/CTCE7_30cm_1m_vol7.wav",
    "../Captures/raw/CTCELC2_30cm_1m_vol7.wav",
    "../Captures/raw/CTCELC2_GluedVol7.wav",
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
    print()

    file_path_wav = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        file_names_wav[i],
    )

    print(file_path_wav)

    if not os.path.isfile(file_path_wav):
        print(file_path_wav, "file likely does not exist")
        continue

    fs, data = scipy.io.wavfile.read(file_path_wav)

    df = pandas.read_csv(
        filepath_or_buffer=file_path,
        sep="\t",
        header=None,
    )
    df.columns = ["begin", "end", "type", "id", "timestamp"]

    # print(df)
    # print()

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
                if begin_timestamp < ZERO:
                    begin_timestamp = ZERO
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

    # print(begin_timestamps)
    # print()
    sequences = []
    if data.ndim == 1:
        for b in begin_timestamps:
            sequences.append(data[int(b * fs) : int(b * fs + 60 * 20 * fs)])
    else:
        for b in begin_timestamps:
            for ch in range(data.shape[1]):
                sequences.append(data[int(b * fs) : int(b * fs + 60 * 20 * fs), ch])

    # t = numpy.arange(0, len(sequences[0])) / fs
    # for index, sequence in enumerate(sequences):
    # if len(sequence) == len(t):
    # pyplot.figure()
    # pyplot.plot(t, sequence)
    # pyplot.title((file_names_wav[i], "sequence number ", str(index)))
    # pyplot.axvline(x=t[30 * fs], color='red', linestyle='--')
    # pyplot.xlabel("time [s]")
    # pyplot.ylabel("amplitude")
    # pyplot.show()
    # else:
    # pyplot.figure()
    # pyplot.plot(t[:-1], sequence)
    # pyplot.title((file_names_wav[i], "sequence number ", str(index)))
    # pyplot.axvline(x=t[30 * fs], color='red', linestyle='--')
    # pyplot.xlabel("time [s]")
    # pyplot.ylabel("amplitude")
    # pyplot.show()

    for index, sequence in enumerate(sequences):
        name = (
            os.path.basename(file_path_wav).split(".")[0]
            + "_"
            + str(index + 1)
            + ".wav"
        )
        file_path_wav = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../Captures/" + name,
        )
        print(file_path_wav)
        scipy.io.wavfile.write(
            file_path_wav, fs, numpy.array(sequence)
        )  # jak tu dodać folder docelowy?


# here is what I expect without subtraction of the offset, but I manualy checked, that it is necessery to substract it
# what i expect from CompactDetectionLog-CTCE7_65dB10cm60dB30cm60dB2m.wav.txt: [47, 1409, 2876] - ok
# what i expect from CompactDetectionLog-CTCELC2_10cmVol9_2.wav.txt: [67.7] - ok
# what i expect from CompactDetectionLog-CTCELCWG2_1_60dB2m.wav.txt: [30.95] - ok
# what i expect from CompactDetectionLog-CTCELCWG2_1_65dB10cm60dB30cm_mic1.wav.txt: [67.7, 1320] - ok
# what i expect from CompactDetectionLog-CTCELCWG2_1_lineIn_VOL50.wav.txt: [1.85] - ok
# what i expect from CompactDetectionLog-KantarCertificationMeters.wav.txt: [0.11] - ok
# what i expect from CompactDetectionLog-CompactDetectionLog-CTCE7_10cmvol9_1.wav.txt: [49.26] - ok
# what i expect from CompactDetectionLog-CompactDetectionLog-CTCE7_10cmvol9_2.wav.txt: [30.18] - ok
# what i expect from CompactDetectionLog-CompactDetectionLog-CTCE7_30cm_1m_vol7.wav.txt: [31.68, 1427.66] - ok
# what i expect from CompactDetectionLog-CompactDetectionLog-CTCELC2_30cm_1m_vol7.wav.txt: [58.43, 1453.93] - ok
# what i expect from CompactDetectionLog-CompactDetectionLog-CTCELC2_GluedVol7.wav.txt: [2.84] - ok
