import pytest


testinfra_hosts = ["akhq"]


def test_service_is_running(service):
    assert service("akhq").is_running


def test_service_is_enabled(service):
    assert service("akhq").is_enabled


def test_akhq_user_exists(user):
    assert user("akhq").exists
    assert user("akhq").shell == "/usr/sbin/nologin"


def test_akhq_group_exists(group):
    assert group("akhq").exists


def test_akhq_directory_permissions(file):
    akhq_dir = file("/opt/akhq-0.25.1")
    assert akhq_dir.exists
    assert akhq_dir.is_directory
    assert akhq_dir.user == "akhq"
    assert akhq_dir.group == "akhq"
    assert oct(akhq_dir.mode) == "0o755"


def test_akhq_is_running_as_akhq(process):
    process_name = "java"
    assert process(process_name).user == "akhq"
    assert process(process_name).group == "akhq"


def test_akhq_is_listening(socket):
    broker = "tcp://0.0.0.0:8080"
    assert socket(broker).is_listening


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
def file(host):
    def _func(path):
        return host.file(path)
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
