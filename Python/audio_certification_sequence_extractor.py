import os
import sys
import numpy
import scipy

from dsp_plotter import DspPlotter


def usage() -> None:
    """
    Displays the help's message

    Args:

    Return:
    None
    """
    print(
        "Usage: python3 ./audio_certification_sequence_extractor.py [-h | -i input *.wav file's path [-o output folder's path | -p [-s]]]"
    )
    print()
    print("         -h                          - display this help's message")
    print(
        "         -i input *.wav file's path  - path of the input *.wav file [mandatory]"
    )
    print(
        "         -o output folder's path     - path of the output folder for the extracted *.wav file(-s) [default is a path of this script's parent folder]"
    )
    print("         -p                          - plot of the input *.wav file's data")
    print(
        "         -s                          - spectrogram of the input *.wav file's data"
    )
    print()


def parse_file(file_path) -> None:
    """
    Parses the input *.wav file

    Args:
    str: file_path

    Return:
    None
    """
    print(file_path)


def plot_file(file_path) -> None:
    """
    Plots the input *.wav file

    Args:
    str: file_path

    Return:
    None
    """
    fs, data = scipy.io.wavfile.read(file_path)
    data = numpy.vstack((data,)) if len(data.shape) == 1 else data.T
    labels = []
    if len(data) == 1:
        labels.append(os.path.basename(file_path))
    else:
        for i in range(len(data)):
            labels.append(os.path.basename(file_path) + f" - channel {i+1}")
    print(fs, data.shape, data.dtype, labels)


def main() -> int:
    """
    Main program's function

    Args:

    Return:
    int: exit code
    """
    print("audio_certification_sequence_extractor v1.0")
    print("Copyright \u00A9 2025 Kantar Media")
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
        os.path.dirname(os.path.abspath(__file__)),
        sys.argv[index + 1],
    )

    if not os.path.isfile(file_path):
        print(file_path, "is not a regular file's path")
        print()
        usage()
        return 1

    if "-p" in sys.argv:
        plot_file(file_path)
        return 0

    parse_file(file_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
