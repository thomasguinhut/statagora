from src.client.dares_client import DaresClient


def test_get_all_dares_ok():
    res = DaresClient().get_all_dares(True)
    assert len(res) == 40
