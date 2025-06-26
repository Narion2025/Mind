import os
import yaml
from modules.marker_grapper import MarkerGrapper
from modules.marker_selfwriter import MarkerSelfwriter
from modules.marker_analyzer import analyze_text_with_grapper


def test_selfwriter_creates_marker(tmp_path):
    # create simple marker file
    marker_dir = tmp_path / "markers"
    marker_dir.mkdir()
    marker_file = marker_dir / "basic.yaml"
    marker_file.write_text(
        "test_marker:\n  muster: ['hello']\n  tags: ['demo']\n", encoding="utf-8"
    )

    grapper = MarkerGrapper(marker_dir=str(marker_dir))
    writer_dir = tmp_path / "writer"
    selfwriter = MarkerSelfwriter(str(writer_dir))

    # text with marker
    hits = analyze_text_with_grapper(grapper, selfwriter, "hello world")
    assert hits == ["test_marker"]
    assert not list(writer_dir.iterdir())

    # text without marker should trigger write
    analyze_text_with_grapper(grapper, selfwriter, "unknown pattern")
    files = list(writer_dir.iterdir())
    assert len(files) == 1
    data = yaml.safe_load(files[0].read_text())
    name = next(iter(data))
    assert data[name]["examples"] == ["unknown pattern"]

