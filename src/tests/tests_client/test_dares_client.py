from client.dares_client import DaresClient


def test_get_all_dares_ok():
    res = DaresClient().get_all_dares(True)
    assert len(res) == 40
    assert (
        res[0]["titre_publication"]
        == "Quelles entreprises recourent à l’alternance, et pour quelles raisons ?"
    )


if __name__ == "__main__":
    import pytest

    pytest.main([__file__])
