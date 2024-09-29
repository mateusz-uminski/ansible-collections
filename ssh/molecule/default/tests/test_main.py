import pytest


def test_is_service_running(service):
    assert service("sshd").is_running


def test_is_service_enabled(service):
    assert service("sshd").is_enabled


def test_sshd_is_running_as_root(process):
    process_name = "sshd"
    assert process(process_name).user == "root"
    assert process(process_name).group == "root"


def test_sshd_is_listening_on_given_port(socket):
    sshd = "tcp://0.0.0.0:22"
    assert socket(sshd).is_listening


@pytest.fixture()
def service(host):
    def _func(service_name):
        return host.service(service_name)
    return _func


@pytest.fixture()
def process(host):
    def _func(process_name):
        return host.process.get(comm=process_name)
    return _func


@pytest.fixture()
def socket(host):
    def _func(spec):
        return host.socket(spec)
    return _func
