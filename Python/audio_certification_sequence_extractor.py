import os
import sys
import numpy
import scipy


def main() -> int:
    file_names = (
        "../Captures/raw/CTCE7_65dB10cm60dB30cm60dB2m.wav",
        "../Captures/raw/CTCELC2_10cmVol9_2.wav",
        "../Captures/raw/CTCELCWG2_1_60dB2m.wav",
        "../Captures/raw/CTCELCWG2_1_65dB10cm60dB30cm_mic1.wav",
        "../Captures/raw/CTCELCWG2_1_lineIn_VOL50.wav",
        "../KantarCertificationMeters.wav",
    )

    for i in range(len(file_names)):
        file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            file_names[i],
        )
        fs, data = scipy.io.wavfile.read(file_path)
        data = numpy.vstack((data,))
        print(file_path, fs, data.shape, len(data))

    return 0


if __name__ == "__main__":
    sys.exit(main())
