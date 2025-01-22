import audio_certification_sequence_extractor


def test_usage() -> None:
    audio_certification_sequence_extractor.usage()


def test_parse_file() -> None:
    audio_certification_sequence_extractor.parse_file(
        "../KantarCertificationMeters.wav"
    )


def test_plot_file() -> None:
    audio_certification_sequence_extractor.plot_file("../KantarCertificationMeters.wav")


def test_main() -> None:
    assert audio_certification_sequence_extractor.main() == 0
