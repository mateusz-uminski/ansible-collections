import pytest


@pytest.mark.parametrize("tool",  [
    "htop",
    "traceroute",
    "ping",
    "dig",
    "gpg",
    "vim",
    "ss",
    "tcpdump"
])
def test_command_is_availablie(host, tool):
    assert host.exists(tool)
