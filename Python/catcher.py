import os
import numpy
import pandas
import scipy


log_file_names = [
    "../LogsSNAP/CompactDetectionLog-CTCE7_65dB10cm60dB30cm60dB2m.wav.txt",
    "../LogsSNAP/CompactDetectionLog-CTCELC2_10cmVol9_2.wav.txt",
    "../LogsSNAP/CompactDetectionLog-CTCELCWG2_1_60dB2m.wav.txt",
    "../LogsSNAP/CompactDetectionLog-CTCELCWG2_1_65dB10cm60dB30cm_mic1.wav.txt",
    "../LogsSNAP/CompactDetectionLog-CTCELCWG2_1_lineIn_VOL50.wav.txt",
    "../LogsSNAP/CompactDetectionLog-KantarCertificationMeters.wav.txt",
    "../LogsSNAP/CompactDetectionLog-CTCE7_10cmvol9_1.wav.txt",
    "../LogsSNAP/CompactDetectionLog-CTCE7_10cmvol9_2.wav.txt",
    "../LogsSNAP/CompactDetectionLog-CTCE7_30cm_1m_vol7.wav.txt",
    "../LogsSNAP/CompactDetectionLog-CTCELC2_30cm_1m_vol7.wav.txt",
    "../LogsSNAP/CompactDetectionLog-CTCELC2_GluedVol7.wav.txt",
]

wav_file_names = [
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

for i in range(len(log_file_names)):
    log_file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        log_file_names[i],
    )

    if not os.path.isfile(log_file_path):
        print(log_file_path, "file likely does not exist!")
        print()
        continue

    print(log_file_path)

    wav_file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        wav_file_names[i],
    )

    if not os.path.isfile(wav_file_path):
        print(wav_file_path, "file likely does not exist!")
        print()
        continue

    print(wav_file_path)
    print()

    df = pandas.read_csv(
        filepath_or_buffer=log_file_path,
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

    print(begin_timestamps)
    print()

    sequences = []
    fs, data = scipy.io.wavfile.read(wav_file_path)

    if data.ndim == 1:
        for begin_timestamp in begin_timestamps:
            sequence = data[
                int(begin_timestamp * fs) : int(begin_timestamp * fs + 60 * 20 * fs)
            ]
            sequences.append(sequence)
    else:
        for begin_timestamp in begin_timestamps:
            inner_sequences = []
            for channel in range(data.shape[1]):
                sequence = data[
                    int(begin_timestamp * fs) : int(
                        begin_timestamp * fs + 60 * 20 * fs
                    ),
                    channel,
                ]
                inner_sequences.append(sequence)
            sequences.append(numpy.array(inner_sequences).T)

    for index, sequence in enumerate(sequences):
        file_name = (
            os.path.basename(wav_file_path).split(".")[0]
            + "_"
            + str(index + 1)
            + ".wav"
        )
        output_file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../Captures",
            file_name,
        )
        scipy.io.wavfile.write(
            output_file_path,
            fs,
            sequence,
        )
        print(output_file_path)

    print()
    print()
