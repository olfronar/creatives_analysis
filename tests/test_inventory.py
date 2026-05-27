from pathlib import Path

from creatives_analysis.inventory import collect_inventory


def test_collect_inventory_reads_all_mp4_metadata() -> None:
    videos = sorted(Path("creatives").glob("*.mp4"))

    rows = collect_inventory(videos)

    assert len(rows) == 5
    assert {row.filename for row in rows} == {
        "ad1.mp4",
        "ad2.mp4",
        "ad3.mp4",
        "ad4.mp4",
        "ad5.mp4",
    }
    assert all(row.duration_seconds > 0 for row in rows)
    assert all(row.has_audio for row in rows)
    assert all(row.orientation == "vertical" for row in rows)
