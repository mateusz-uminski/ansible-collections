import pytest


def test_default_firewalls_are_disabled(distribution, service):
    if distribution() == "debian":
        assert not service("ufw").is_running
        assert not service("ufw").is_enabled

    if distribution() == "redhat":
        assert not service("firewalld").is_running
        assert not service("firewalld").is_enabled


def test_is_service_running(service):
    assert service("iptables-rules").is_running


def test_is_service_enabled(service):
    assert service("iptables-rules").is_enabled


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


@pytest.fixture()
def distribution(host):
    def _func():
        return host.system_info.distribution
    return _func
