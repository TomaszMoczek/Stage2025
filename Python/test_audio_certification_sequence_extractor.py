import os
import numpy as np
import audio_certification_sequence_extractor


def test_usage() -> None:
    audio_certification_sequence_extractor.usage()


def test_get_begin_timestamps_CTCE7_10cmvol9_1() -> None:
    assert audio_certification_sequence_extractor.get_begin_timestamps(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../LogsSNAP/CompactDetectionLog-CTCE7_10cmvol9_1.wav.txt",
        )
    ) == [np.float64(49.17999999999999)]


def test_get_begin_timestamps_CTCE7_10cmvol9_2() -> None:
    assert audio_certification_sequence_extractor.get_begin_timestamps(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../LogsSNAP/CompactDetectionLog-CTCE7_10cmvol9_2.wav.txt",
        )
    ) == [np.float64(30.040000000000006)]


def test_get_begin_timestamps_CTCE7_30cm_1m_vol7() -> None:
    assert audio_certification_sequence_extractor.get_begin_timestamps(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../LogsSNAP/CompactDetectionLog-CTCE7_30cm_1m_vol7.wav.txt",
        )
    ) == [np.float64(31.680000000000007), np.float64(1426.98)]


def test_get_begin_timestamps_CTCE7_65dB10cm60dB30cm60dB2m() -> None:
    assert audio_certification_sequence_extractor.get_begin_timestamps(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../LogsSNAP/CompactDetectionLog-CTCE7_65dB10cm60dB30cm60dB2m.wav.txt",
        )
    ) == [np.float64(47.379999999999995), np.float64(1409.23), np.float64(2875.93)]


def test_get_begin_timestamps_CTCELC2_10cmVol9_2() -> None:
    assert audio_certification_sequence_extractor.get_begin_timestamps(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../LogsSNAP/CompactDetectionLog-CTCELC2_10cmVol9_2.wav.txt",
        )
    ) == [np.float64(67.6)]


def test_get_begin_timestamps_CTCELC2_30cm_1m_vol7() -> None:
    assert audio_certification_sequence_extractor.get_begin_timestamps(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../LogsSNAP/CompactDetectionLog-CTCELC2_30cm_1m_vol7.wav.txt",
        )
    ) == [np.float64(58.42000000000001), np.float64(1453.7)]


def test_get_begin_timestamps_CTCELC2_GluedVol7() -> None:
    assert audio_certification_sequence_extractor.get_begin_timestamps(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../LogsSNAP/CompactDetectionLog-CTCELC2_GluedVol7.wav.txt",
        )
    ) == [np.float64(2.7200000000000033)]


def test_get_begin_timestamps_CTCELCWG2_1_60dB2m() -> None:
    assert audio_certification_sequence_extractor.get_begin_timestamps(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../LogsSNAP/CompactDetectionLog-CTCELCWG2_1_60dB2m.wav.txt",
        )
    ) == [np.float64(28.890000000000004)]


def test_get_begin_timestamps_CTCELCWG2_1_65dB10cm60dB30cm_mic1() -> None:
    assert audio_certification_sequence_extractor.get_begin_timestamps(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../LogsSNAP/CompactDetectionLog-CTCELCWG2_1_65dB10cm60dB30cm_mic1.wav.txt",
        )
    ) == [np.float64(67.61999999999999), np.float64(1321.44)]


def test_get_begin_timestamps_CTCELCWG2_1_lineIn_VOL50() -> None:
    assert audio_certification_sequence_extractor.get_begin_timestamps(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../LogsSNAP/CompactDetectionLog-CTCELCWG2_1_lineIn_VOL50.wav.txt",
        )
    ) == [np.float64(1.8499999999999943)]


def test_get_begin_timestamps_KantarCertificationMeters() -> None:
    assert audio_certification_sequence_extractor.get_begin_timestamps(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../LogsSNAP/CompactDetectionLog-KantarCertificationMeters.wav.txt",
        )
    ) == [np.float64(0.0)]


def test_parse_file() -> None:
    audio_certification_sequence_extractor.parse_file(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../Captures/raw/CTCE7_65dB10cm60dB30cm60dB2m.wav",
        )
    )


def test_plot_file() -> None:
    audio_certification_sequence_extractor.plot_file(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../Captures/raw/CTCE7_65dB10cm60dB30cm60dB2m.wav",
        )
    )


def test_main() -> None:
    assert audio_certification_sequence_extractor.main() == 1
