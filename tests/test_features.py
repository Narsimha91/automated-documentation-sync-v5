from src.features import FEATURES, features


def test_features_returns_configured_features() -> None:
    assert FEATURES == ["Create", "Update", "Read"]
    assert features() == ["Create", "Update", "Read"]