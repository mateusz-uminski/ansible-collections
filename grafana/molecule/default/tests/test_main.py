import pytest


def test_service_is_running(service):
    assert service("grafana-server").is_running


def test_service_is_enabled(service):
    assert service("grafana-server").is_enabled


def test_grafana_user_exists(distribution, user):
    nologin_shell = "/sbin/nologin"
    if distribution() == "debian":
        nologin_shell = "/bin/false"

    assert user("grafana").exists
    assert user("grafana").shell == nologin_shell


def test_grafana_group_exists(group):
    assert group("grafana").exists


def test_grafana_is_running_as_grafana(process):
    process_name = "grafana"
    assert process(process_name).user == "grafana"
    assert process(process_name).group == "grafana"


def test_grafana_is_listening(socket):
    grafana_ui = "tcp://0.0.0.0:3000"
    assert socket(grafana_ui).is_listening


@pytest.fixture()
def service(host):
    def _func(service_name):
        return host.service(service_name)
    return _func


@pytest.fixture()
def user(host):
    def _func(user_name):
        return host.user(user_name)
    return _func


@pytest.fixture()
def group(host):
    def _func(group_name):
        return host.group(group_name)
    return _func


@pytest.fixture()
def distribution(host):
    def _func():
        return host.system_info.distribution
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
