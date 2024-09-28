import pytest


def test_service_is_running(service):
    assert service("vault").is_running


def test_service_is_enabled(service):
    assert service("vault").is_enabled


def test_vault_user_exists(user):
    assert user("vault").exists
    assert user("vault").shell == "/bin/false"


def test_vault_group_exists(group):
    assert group("vault").exists


def test_vault_config_permissions(file):
    vault_cfg = file("/etc/vault.d/vault.hcl")
    assert vault_cfg.exists
    assert vault_cfg.user == "vault"
    assert vault_cfg.group == "vault"
    assert oct(vault_cfg.mode) == "0o644"


def test_vault_is_running_as_vault(process):
    process_name = "vault"
    assert process(process_name).user == "vault"
    assert process(process_name).group == "vault"


def test_vault_command_is_availablie(host):
    assert host.exists("vault")


def test_vault_is_listening_on_ports(socket):
    sockets = {
        'vault_api_addr': "tcp://0.0.0.0:8200",
        'vault_cluster_addr': "tcp://0.0.0.0:8201",
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
