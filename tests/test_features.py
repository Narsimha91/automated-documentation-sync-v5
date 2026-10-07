from src.features import FEATURES, features


def test_features_returns_configured_features() -> None:
    assert FEATURES == ["Create", "Update", "READ"]
    assert features() == ["Create", "Update", "READ"]