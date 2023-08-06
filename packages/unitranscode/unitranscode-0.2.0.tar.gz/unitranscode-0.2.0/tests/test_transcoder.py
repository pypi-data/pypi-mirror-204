from os.path import isfile
from pathlib import Path


from unitranscode.transcoder import Transcoder


def test_edit(example_20s_wav_file: Path, temp_folder: Path):
    in_file = example_20s_wav_file
    transcoder = Transcoder()

    cuts = [(0.0, 1.0), (3.0, 4.5), (7.0, 10.0)]

    out_file = transcoder.edit(
        in_file, cuts, temp_folder.joinpath('output.wav')
    )

    assert isfile(out_file)

    in_file_duration = transcoder.info(in_file).duration_s
    out_file_duration = transcoder.info(out_file).duration_s
    expected_duration = sum([end - start for start, end in cuts])
    assert abs(expected_duration - out_file_duration) < 0.1 * in_file_duration
