from pathlib import Path

from creatives_analysis.inventory import collect_inventory

from tests.helpers import make_test_video


def test_collect_inventory_reads_all_mp4_metadata(tmp_path: Path) -> None:
    videos = [
        make_test_video(tmp_path, "ad1.mp4"),
        make_test_video(tmp_path, "ad2.mp4"),
    ]

    rows = collect_inventory(videos)

    assert len(rows) == 2
    assert {row.filename for row in rows} == {
        "ad1.mp4",
        "ad2.mp4",
    }
    assert all(row.duration_seconds > 0 for row in rows)
    assert all(row.has_audio for row in rows)
    assert all(row.orientation == "vertical" for row in rows)
