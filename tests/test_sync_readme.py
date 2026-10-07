from pathlib import Path

import pytest

from scripts.sync_readme import END_MARKER, START_MARKER, render_features, sync_readme


def test_render_features_keeps_order_and_normalizes_line_breaks() -> None:
    assert render_features(["Create", "New\r\nfeature"]) == "- Create\n- New feature"


def test_render_features_allows_empty_list_and_blank_names() -> None:
    assert render_features([]) == ""
    assert render_features([""]) == "- "


def test_sync_readme_preserves_content_outside_markers(tmp_path: Path) -> None:
    prefix = f"Header\r\n{START_MARKER}"
    suffix = f"{END_MARKER}\r\nFooter"
    readme_path = tmp_path / "README.md"
    readme_path.write_bytes(f"{prefix}\r\nold feature\r\n{suffix}".encode("utf-8"))

    assert sync_readme(readme_path, ["Create", "Update"])

    updated = readme_path.read_bytes()
    updated_text = updated.decode("utf-8")
    assert updated_text.startswith(prefix)
    assert updated_text.endswith(suffix)
    assert f"{START_MARKER}\n- Create\n- Update\n{END_MARKER}" in updated_text


@pytest.mark.parametrize(
    "readme_text",
    [
        "No markers",
        f"{START_MARKER}\ncontent",
        f"{END_MARKER}\ncontent",
        f"{START_MARKER}\n{START_MARKER}\n{END_MARKER}",
        f"{START_MARKER}\n{END_MARKER}\n{END_MARKER}",
        f"{END_MARKER}\n{START_MARKER}",
    ],
)
def test_sync_readme_rejects_invalid_markers_without_writing(
    tmp_path: Path, readme_text: str
) -> None:
    readme_path = tmp_path / "README.md"
    original = readme_text.encode("utf-8")
    readme_path.write_bytes(original)

    with pytest.raises(ValueError):
        sync_readme(readme_path, ["Create"])

    assert readme_path.read_bytes() == original


def test_sync_readme_does_not_write_when_features_are_current(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    readme_path = tmp_path / "README.md"
    current = f"{START_MARKER}\n- Create\n- Update\n{END_MARKER}".encode("utf-8")
    readme_path.write_bytes(current)

    def fail_if_written(path: Path, data: bytes) -> int:
        pytest.fail("sync_readme should not write an unchanged README")

    monkeypatch.setattr(Path, "write_bytes", fail_if_written)
    assert not sync_readme(readme_path, ["Create", "Update"])