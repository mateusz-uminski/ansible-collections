import pytest


def test_service_is_running(service):
    assert service("tempo").is_running


def test_service_is_enabled(service):
    assert service("tempo").is_enabled


def test_tempo_user_exists(user):
    assert user("tempo").exists
    assert user("tempo").shell == "/usr/sbin/nologin"


def test_tempo_group_exists(group):
    assert group("tempo").exists


def test_tempo_config_directory_permissions(file):
    tempo_cfg_dir = file("/etc/tempo")
    assert tempo_cfg_dir.exists
    assert tempo_cfg_dir.is_directory
    assert tempo_cfg_dir.user == "tempo"
    assert tempo_cfg_dir.group == "tempo"
    assert oct(tempo_cfg_dir.mode) == "0o755"


def test_tempo_storage_directory_permissions(file):
    tempo_storage_dir = file("/tmp/tempo")
    assert tempo_storage_dir.exists
    assert tempo_storage_dir.is_directory
    assert tempo_storage_dir.user == "tempo"
    assert tempo_storage_dir.group == "tempo"
    assert oct(tempo_storage_dir.mode) == "0o755"


def test_tempo_is_running_as_tempo(process):
    process_name = "tempo"
    assert process(process_name).user == "tempo"
    assert process(process_name).group == "tempo"


def test_tempo_config_permissions(file):
    tempo_cfg = file("/etc/tempo/config.yaml")
    assert tempo_cfg.exists
    assert tempo_cfg.user == "tempo"
    assert tempo_cfg.group == "tempo"
    assert oct(tempo_cfg.mode) == "0o644"


def test_tempo_is_listening_on_ports(socket):
    sockets = {
        'tempo_http': "tcp://0.0.0.0:3200",
        'tempo_grpc': "tcp://0.0.0.0:9095",
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
