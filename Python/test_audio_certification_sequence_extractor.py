import os
import audio_certification_sequence_extractor


def test_usage() -> None:
    audio_certification_sequence_extractor.usage()


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
