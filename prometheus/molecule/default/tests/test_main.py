import pytest


def test_service_is_running(service):
    assert service("prometheus").is_running


def test_service_is_enabled(service):
    assert service("prometheus").is_enabled


def test_prometheus_user_exists(user):
    assert user("prometheus").exists
    assert user("prometheus").shell == "/usr/sbin/nologin"


def test_prometheus_group_exists(group):
    assert group("prometheus").exists


def test_prometheus_config_directory_permissions(file):
    prometheus_cfg_dir = file("/etc/prometheus")
    assert prometheus_cfg_dir.exists
    assert prometheus_cfg_dir.is_directory
    assert prometheus_cfg_dir.user == "prometheus"
    assert prometheus_cfg_dir.group == "prometheus"
    assert oct(prometheus_cfg_dir.mode) == "0o755"


def test_prometheus_storage_directory_permissions(file):
    prometheus_storage_dir = file("/var/lib/prometheus")
    assert prometheus_storage_dir.exists
    assert prometheus_storage_dir.is_directory
    assert prometheus_storage_dir.user == "prometheus"
    assert prometheus_storage_dir.group == "prometheus"
    assert oct(prometheus_storage_dir.mode) == "0o755"


def test_prometheus_config_permissions(file):
    prometheus_cfg = file("/etc/prometheus/prometheus.yaml")
    assert prometheus_cfg.exists
    assert prometheus_cfg.user == "prometheus"
    assert prometheus_cfg.group == "prometheus"
    assert oct(prometheus_cfg.mode) == "0o644"


def test_prometheus_is_running_as_prometheus(process):
    process_name = "prometheus"
    assert process(process_name).user == "prometheus"
    assert process(process_name).group == "prometheus"


def test_prometheus_is_listening(socket):
    prometheus = "tcp://0.0.0.0:9090"
    assert socket(prometheus).is_listening


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
