import os
import numpy as np
import audio_certification_sequence_extractor


def test_usage() -> None:
    audio_certification_sequence_extractor.usage()


def test_get_begin_timestamps_CTCE7_10cmvol9_1() -> None:
    assert audio_certification_sequence_extractor.get_begin_timestamps(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../Captures/raw/CTCE7_10cmvol9_1.wav",
        )
    ) == [np.float64(49.17999999999999)]


def test_get_begin_timestamps_CTCE7_10cmvol9_2() -> None:
    assert audio_certification_sequence_extractor.get_begin_timestamps(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../Captures/raw/CTCE7_10cmvol9_2.wav",
        )
    ) == [np.float64(30.040000000000006)]


def test_get_begin_timestamps_CTCE7_30cm_1m_vol7() -> None:
    assert audio_certification_sequence_extractor.get_begin_timestamps(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../Captures/raw/CTCE7_30cm_1m_vol7.wav",
        )
    ) == [np.float64(31.680000000000007), np.float64(1426.98)]


def test_get_begin_timestamps_CTCE7_65dB10cm60dB30cm60dB2m() -> None:
    assert audio_certification_sequence_extractor.get_begin_timestamps(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../Captures/raw/CTCE7_65dB10cm60dB30cm60dB2m.wav",
        )
    ) == [np.float64(47.379999999999995), np.float64(1409.23), np.float64(2875.93)]


def test_get_begin_timestamps_CTCELC2_10cmVol9_2() -> None:
    assert audio_certification_sequence_extractor.get_begin_timestamps(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../Captures/raw/CTCELC2_10cmVol9_2.wav",
        )
    ) == [np.float64(67.6)]


def test_get_begin_timestamps_CTCELC2_30cm_1m_vol7() -> None:
    assert audio_certification_sequence_extractor.get_begin_timestamps(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../Captures/raw/CTCELC2_30cm_1m_vol7.wav",
        )
    ) == [np.float64(58.42000000000001), np.float64(1453.7)]


def test_get_begin_timestamps_CTCELC2_GluedVol7() -> None:
    assert audio_certification_sequence_extractor.get_begin_timestamps(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../Captures/raw/CTCELC2_GluedVol7.wav",
        )
    ) == [np.float64(2.7200000000000033)]


def test_get_begin_timestamps_CTCELCWG2_1_60dB2m() -> None:
    assert audio_certification_sequence_extractor.get_begin_timestamps(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../Captures/raw/CTCELCWG2_1_60dB2m.wav",
        )
    ) == [np.float64(28.890000000000004)]


def test_get_begin_timestamps_CTCELCWG2_1_65dB10cm60dB30cm_mic1() -> None:
    assert audio_certification_sequence_extractor.get_begin_timestamps(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../Captures/raw/CTCELCWG2_1_65dB10cm60dB30cm_mic1.wav",
        )
    ) == [np.float64(67.61999999999999), np.float64(1321.44)]


def test_get_begin_timestamps_CTCELCWG2_1_lineIn_VOL50() -> None:
    assert audio_certification_sequence_extractor.get_begin_timestamps(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../Captures/raw/CTCELCWG2_1_lineIn_VOL50.wav",
        )
    ) == [np.float64(1.8499999999999943)]


def test_get_begin_timestamps_KantarCertificationMeters() -> None:
    assert audio_certification_sequence_extractor.get_begin_timestamps(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../KantarCertificationMeters.wav",
        )
    ) == [np.float64(0.0)]


def test_extract_sequence_files_CTCE7_10cmvol9_1() -> None:
    begin_timestamps = [np.float64(49.17999999999999)]
    output_file_paths = audio_certification_sequence_extractor.extract_sequence_files(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../Captures/raw/CTCE7_10cmvol9_1.wav",
        ),
        begin_timestamps,
    )
    assert len(output_file_paths) == len(begin_timestamps)
    for i in range(len(output_file_paths)):
        assert os.path.isfile(output_file_paths[i])


def test_extract_sequence_files_CTCE7_10cmvol9_2() -> None:
    begin_timestamps = [np.float64(30.040000000000006)]
    output_file_paths = audio_certification_sequence_extractor.extract_sequence_files(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../Captures/raw/CTCE7_10cmvol9_2.wav",
        ),
        begin_timestamps,
    )
    assert len(output_file_paths) == len(begin_timestamps)
    for i in range(len(output_file_paths)):
        assert os.path.isfile(output_file_paths[i])


def test_extract_sequence_files_CTCE7_30cm_1m_vol7() -> None:
    begin_timestamps = [np.float64(31.680000000000007), np.float64(1426.98)]
    output_file_paths = audio_certification_sequence_extractor.extract_sequence_files(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../Captures/raw/CTCE7_30cm_1m_vol7.wav",
        ),
        begin_timestamps,
    )
    assert len(output_file_paths) == len(begin_timestamps)
    for i in range(len(output_file_paths)):
        assert os.path.isfile(output_file_paths[i])


def test_extract_sequence_files_CTCE7_65dB10cm60dB30cm60dB2m() -> None:
    begin_timestamps = [
        np.float64(47.379999999999995),
        np.float64(1409.23),
        np.float64(2875.93),
    ]
    output_file_paths = audio_certification_sequence_extractor.extract_sequence_files(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../Captures/raw/CTCE7_65dB10cm60dB30cm60dB2m.wav",
        ),
        begin_timestamps,
    )
    assert len(output_file_paths) == len(begin_timestamps)
    for i in range(len(output_file_paths)):
        assert os.path.isfile(output_file_paths[i])


def test_extract_sequence_files_CTCELC2_10cmVol9_2() -> None:
    begin_timestamps = [np.float64(67.6)]
    output_file_paths = audio_certification_sequence_extractor.extract_sequence_files(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../Captures/raw/CTCELC2_10cmVol9_2.wav",
        ),
        begin_timestamps,
    )
    assert len(output_file_paths) == len(begin_timestamps)
    for i in range(len(output_file_paths)):
        assert os.path.isfile(output_file_paths[i])


def test_extract_sequence_files_CTCELC2_30cm_1m_vol7() -> None:
    begin_timestamps = [np.float64(58.42000000000001), np.float64(1453.7)]
    output_file_paths = audio_certification_sequence_extractor.extract_sequence_files(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../Captures/raw/CTCELC2_30cm_1m_vol7.wav",
        ),
        begin_timestamps,
    )
    assert len(output_file_paths) == len(begin_timestamps)
    for i in range(len(output_file_paths)):
        assert os.path.isfile(output_file_paths[i])


def test_extract_sequence_files_CTCELC2_GluedVol7() -> None:
    begin_timestamps = [np.float64(2.7200000000000033)]
    output_file_paths = audio_certification_sequence_extractor.extract_sequence_files(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../Captures/raw/CTCELC2_GluedVol7.wav",
        ),
        begin_timestamps,
    )
    assert len(output_file_paths) == len(begin_timestamps)
    for i in range(len(output_file_paths)):
        assert os.path.isfile(output_file_paths[i])


def test_extract_sequence_files_CTCELCWG2_1_60dB2m() -> None:
    begin_timestamps = [np.float64(28.890000000000004)]
    output_file_paths = audio_certification_sequence_extractor.extract_sequence_files(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../Captures/raw/CTCELCWG2_1_60dB2m.wav",
        ),
        begin_timestamps,
    )
    assert len(output_file_paths) == len(begin_timestamps)
    for i in range(len(output_file_paths)):
        assert os.path.isfile(output_file_paths[i])


def test_extract_sequence_files_CTCELCWG2_1_65dB10cm60dB30cm_mic1() -> None:
    begin_timestamps = [np.float64(67.61999999999999), np.float64(1321.44)]
    output_file_paths = audio_certification_sequence_extractor.extract_sequence_files(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../Captures/raw/CTCELCWG2_1_65dB10cm60dB30cm_mic1.wav",
        ),
        begin_timestamps,
    )
    assert len(output_file_paths) == len(begin_timestamps)
    for i in range(len(output_file_paths)):
        assert os.path.isfile(output_file_paths[i])


def test_extract_sequence_files_CTCELCWG2_1_lineIn_VOL50() -> None:
    begin_timestamps = [np.float64(1.8499999999999943)]
    output_file_paths = audio_certification_sequence_extractor.extract_sequence_files(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../Captures/raw/CTCELCWG2_1_lineIn_VOL50.wav",
        ),
        begin_timestamps,
    )
    assert len(output_file_paths) == len(begin_timestamps)
    for i in range(len(output_file_paths)):
        assert os.path.isfile(output_file_paths[i])


def test_extract_sequence_files_KantarCertificationMeters() -> None:
    begin_timestamps = [np.float64(0.0)]
    output_file_paths = audio_certification_sequence_extractor.extract_sequence_files(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../KantarCertificationMeters.wav",
        ),
        begin_timestamps,
    )
    assert len(output_file_paths) == len(begin_timestamps)
    for i in range(len(output_file_paths)):
        assert os.path.isfile(output_file_paths[i])


def test_extract_sequence_files_incorrect_file_path() -> None:
    begin_timestamps = [np.float64(0.0)]
    output_file_paths = audio_certification_sequence_extractor.extract_sequence_files(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../incorrect_file.wav",
        ),
        begin_timestamps,
    )
    assert output_file_paths == []


def test_extract_sequence_files_empty_begin_timestamps() -> None:
    begin_timestamps = []
    output_file_paths = audio_certification_sequence_extractor.extract_sequence_files(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../KantarCertificationMeters.wav",
        ),
        begin_timestamps,
    )
    assert output_file_paths == []


def test_main() -> None:
    assert audio_certification_sequence_extractor.main() == 1
