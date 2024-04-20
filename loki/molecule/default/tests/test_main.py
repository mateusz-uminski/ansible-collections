import pytest


def test_service_is_running(service):
    assert service("loki").is_running


def test_service_is_enabled(service):
    assert service("loki").is_enabled


def test_loki_user_exists(user):
    assert user("loki").exists
    assert user("loki").shell == "/usr/sbin/nologin"


def test_loki_group_exists(group):
    assert group("loki").exists


def test_loki_config_directory_permissions(file):
    loki_cfg_dir = file("/etc/loki")
    assert loki_cfg_dir.exists
    assert loki_cfg_dir.is_directory
    assert loki_cfg_dir.user == "loki"
    assert loki_cfg_dir.group == "loki"
    assert oct(loki_cfg_dir.mode) == "0o755"


def test_loki_storage_directory_permissions(file):
    loki_storage_dir = file("/etc/loki")
    assert loki_storage_dir.exists
    assert loki_storage_dir.is_directory
    assert loki_storage_dir.user == "loki"
    assert loki_storage_dir.group == "loki"
    assert oct(loki_storage_dir.mode) == "0o755"


def test_loki_is_running_as_loki(process):
    process_name = "loki"
    assert process(process_name).user == "loki"
    assert process(process_name).group == "loki"


def test_loki_config_permissions(file):
    loki_cfg = file("/etc/loki/config.yaml")
    assert loki_cfg.exists
    assert loki_cfg.user == "loki"
    assert loki_cfg.group == "loki"
    assert oct(loki_cfg.mode) == "0o644"


def test_loki_is_listening_on_ports(socket):
    sockets = {
        'loki_http': "tcp://0.0.0.0:3100",
        'loki_grpc': "tcp://0.0.0.0:9096",
    }
    for _, s in sockets.items():
        assert socket(s).is_listening


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
