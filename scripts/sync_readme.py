from pathlib import Path

from src.features import features

START_MARKER = "<!-- docs-sync: start -->"
END_MARKER = "<!-- docs-sync: end -->"


def render_features(feature_names: list[str]) -> str:
    normalized_names = [
        name.replace("\r\n", " ").replace("\r", " ").replace("\n", " ")
        for name in feature_names
    ]
    return "\n".join(f"- {name}" for name in normalized_names)


def sync_readme(readme_path: Path, feature_names: list[str]) -> bool:
    original_bytes = readme_path.read_bytes()
    original_text = original_bytes.decode("utf-8")

    if original_text.count(START_MARKER) != 1:
        raise ValueError("README must contain exactly one docs-sync start marker")
    if original_text.count(END_MARKER) != 1:
        raise ValueError("README must contain exactly one docs-sync end marker")

    start_position = original_text.index(START_MARKER)
    end_position = original_text.index(END_MARKER)
    if start_position >= end_position:
        raise ValueError("README docs-sync markers are out of order")

    content_start = start_position + len(START_MARKER)
    replacement = f"\n{render_features(feature_names)}\n"
    updated_text = original_text[:content_start] + replacement + original_text[end_position:]
    updated_bytes = updated_text.encode("utf-8")

    if updated_bytes == original_bytes:
        return False

    readme_path.write_bytes(updated_bytes)
    return True


def main() -> None:
    readme_path = Path(__file__).resolve().parents[1] / "README.md"
    if sync_readme(readme_path, features()):
        print("README feature list updated")
    else:
        print("README feature list is already current")


if __name__ == "__main__":
    main()