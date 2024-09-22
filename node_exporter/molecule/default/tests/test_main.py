import pytest


def test_service_is_running(service):
    assert service("node-exporter").is_running


def test_service_is_enabled(service):
    assert service("node-exporter").is_enabled


def test_nodeexporter_user_exists(user):
    assert user("nodeexporter").exists
    assert user("nodeexporter").shell == "/usr/sbin/nologin"


def test_nodeexporter_group_exists(group):
    assert group("nodeexporter").exists


def test_node_exporter_is_running_as_nodeexporter(process):
    process_name = "node-exporter"
    assert process(process_name).user == "nodeexporter"
    assert process(process_name).group == "nodeexporter"


def test_node_exporter_is_listening(socket):
    node_exporter = "tcp://0.0.0.0:9100"
    assert socket(node_exporter).is_listening


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
def process(host):
    def _func(process_name):
        return host.process.get(comm=process_name)
    return _func


@pytest.fixture()
def socket(host):
    def _func(spec):
        return host.socket(spec)
    return _func
