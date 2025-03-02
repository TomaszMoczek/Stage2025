import os
import sys
import numpy
import scipy
import pandas
import subprocess

from termcolor import colored


def usage() -> None:
    """
    Displays the help's message

    Args:

    Return:
    None
    """
    print(
        "Usage: python audio_certification_sequence_extractor.py [-h | -i input *.wav file's path [-o output folder's path]]"
    )
    print()
    print("         -h                          - display this help's message")
    print(
        "         -i input *.wav file's path  - path of the input *.wav file [mandatory]"
    )
    print(
        "         -o output folder's path     - path of the output folder for the extracted *.wav file(-s) [default is a path of the current working directory]"
    )
    print()


def get_begin_timestamps(file_path) -> list:
    """
    Parses the input CompactDetectionLog.txt file

    Args:
    str: file_path

    Return:
    list: begin_timestamps
    """
    begin_timestamps = []

    if not os.path.isfile(file_path):
        print(file_path, "file likely does not exist")
        return begin_timestamps

    sample_reader = subprocess.run(
        [
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "../SamplesAudioWM/Sample_Reader.exe",
            ),
            "-i",
            file_path,
            "-type",
            "SNAP",
            "-profile",
            "P5T",
        ],
        capture_output=True,
        start_new_session=True,
    )

    if sample_reader.returncode != 0:
        print(f"Sample_Reader.exe exited with {sample_reader.returncode} return code:")
        print(f"{sample_reader.stderr.decode()}")
        return begin_timestamps

    df = pandas.read_csv(
        filepath_or_buffer=os.path.join(
            os.getcwd(),
            "./CompactDetectionLog.txt",
        ),
        sep="\t",
        header=None,
    )
    df.columns = ["begin", "end", "type", "id", "timestamp"]

    flag = False
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

    return begin_timestamps


def extract_sequence_files(file_path, begin_timestamps, output_folder_path) -> dict:
    """
    Extracts the output audio sequence files from the input *.wav file

    Args:
    str: file_path
    list: begin_timestamps
    str: output_folder_path

    Return:
    dict: output_file_paths
    """
    output_file_paths = {}

    if not os.path.isfile(file_path):
        print(file_path, "file likely does not exist")
        return output_file_paths

    distances = []
    sequences = []

    positions = {
        "linein": -1,
        "glued": -1,
        "10cm": -1,
        "30cm": -1,
        "1m": -1,
        "2m": -1,
        "3m": -1,
    }

    file_name = str(os.path.basename(file_path)).lower()

    for position in positions.keys():
        positions[position] = file_name.find(position)

    positions = {k: v for k, v in positions.items() if v != -1}
    positions = dict(sorted(positions.items(), key=lambda item: item[1]))

    distances = list(positions.keys())

    fs, data = scipy.io.wavfile.read(file_path)

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

    modes = {
        "linein": "2",
        "glued": "2",
        "10cm": "3",
        "30cm": "4",
        "1m": "4",
        "2m": "4",
        "3m": "4",
    }

    flag = len(distances) == len(sequences)

    for index, sequence in enumerate(sequences):
        file_name = (
            os.path.basename(file_path).split(".")[0] + "_" + str(index + 1) + ".wav"
        )
        output_file_path = os.path.join(
            output_folder_path,
            file_name,
        )
        scipy.io.wavfile.write(
            output_file_path,
            fs,
            sequence,
        )
        print("Extracted output file: ", output_file_path)
        types = ("SNAP", "KAM_ID_INK")
        mode = modes[distances[index]] if flag else modes["linein"]
        if not os.path.isdir(os.path.join(output_folder_path, "SNAP")):
            os.mkdir(os.path.join(output_folder_path, "SNAP"))
        if not os.path.isdir(os.path.join(output_folder_path, "KAM_ID_INK")):
            os.mkdir(os.path.join(output_folder_path, "KAM_ID_INK"))
        for type in types:
            sample_reader = subprocess.run(
                [
                    os.path.join(
                        os.path.dirname(os.path.abspath(__file__)),
                        "../SamplesAudioWM/Sample_Reader.exe",
                    ),
                    "-i",
                    output_file_path,
                    "-type",
                    type,
                    "-profile",
                    "P5T",
                    "-certificationMode",
                    mode,
                ],
                capture_output=True,
                start_new_session=True,
            )
            if sample_reader.returncode != 0:
                print(
                    f"Sample_Reader.exe exited with {sample_reader.returncode} return code:"
                )
                print(f"{sample_reader.stderr.decode()}")
            else:
                if type == "SNAP":
                    for file in os.listdir(output_folder_path):
                        if file.endswith(".txt"):
                            if "MainReport" in file:
                                report = pandas.read_csv(
                                    os.path.join(output_folder_path, file), header=None
                                )
                                print(colored("SNAP Certification Results:", "blue"))
                                if report.loc[4, 0].split()[2] == "YES":
                                    print(colored(report.loc[4, 0], "green"))
                                else:
                                    print(colored(report.loc[4, 0], "red"))
                                    for i in range(6, 11):
                                        if report.loc[i, 0].split()[2] == "KO":
                                            print(colored(report.loc[i, 0], "red"))
                            os.rename(
                                os.path.join(output_folder_path, file),
                                os.path.join(output_folder_path, "SNAP", file),
                            )
                elif type == "KAM_ID_INK":
                    for file in os.listdir(output_folder_path):
                        if file.endswith(".txt"):
                            if "MainReport" in file:
                                report = pandas.read_csv(
                                    os.path.join(output_folder_path, file), header=None
                                )
                                print(
                                    colored("KAM_ID_INK Certification Results:", "blue")
                                )
                                if report.loc[4, 0].split()[2] == "YES":
                                    print(colored(report.loc[4, 0], "green"))
                                else:
                                    print(colored(report.loc[4, 0], "red"))
                                    for i in range(6, 11):
                                        if report.loc[i, 0].split()[2] == "KO":
                                            print(colored(report.loc[i, 0], "red"))
                            os.rename(
                                os.path.join(output_folder_path, file),
                                os.path.join(output_folder_path, "KAM_ID_INK", file),
                            )
        print()
        output_file_paths[output_file_path] = mode

    return output_file_paths


def parse_file(file_path, output_folder_path) -> None:
    """
    Parses the input *.wav file

    Args:
    str: file_path
    str: output_folder_path

    Return:
    None
    """
    print("Parsing input file: ", file_path)
    print()
    begin_timestamps = get_begin_timestamps(file_path=file_path)
    if len(begin_timestamps) == 0:
        print("Failed to parse input file: ", file_path)
        return
    extract_sequence_files(
        file_path=file_path,
        begin_timestamps=begin_timestamps,
        output_folder_path=output_folder_path,
    )
    print("Done")


def main() -> int:
    """
    Main program's function

    Args:

    Return:
    int: exit code
    """
    print("audio_certification_sequence_extractor v1.0")
    print("Copyright \u00A9 2025 Kantar Media Audiences Limited. All rights reserved.")
    print()

    if len(sys.argv) == 1 or "-h" in sys.argv:
        usage()
        return 0

    if "-i" not in sys.argv:
        print("-i command line argument is missing")
        print()
        usage()
        return 1

    index = sys.argv.index("-i")

    if len(sys.argv) < index + 2:
        print("input *.wav file's path command line argument is missing")
        print()
        usage()
        return 1

    file_path = os.path.join(
        os.getcwd(),
        sys.argv[index + 1],
    )

    if not os.path.isfile(file_path):
        print(file_path, "is not a regular file's path")
        print()
        usage()
        return 1

    output_folder_path = os.getcwd()

    if "-o" in sys.argv:
        index = sys.argv.index("-o")

        if len(sys.argv) < index + 2:
            print("output folder's path command line argument is missing")
            print()
            usage()
            return 1

        output_folder_path = os.path.join(
            os.getcwd(),
            sys.argv[index + 1],
        )

        if not os.path.isdir(output_folder_path):
            print(output_folder_path, "is not a regular directory's path")
            print()
            usage()
            return 1

    parse_file(file_path, output_folder_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
