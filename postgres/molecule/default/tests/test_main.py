import pytest


def test_service_is_running(service):
    assert service("postgresql").is_running


def test_service_is_enabled(service):
    assert service("postgresql").is_enabled


def test_postgres_user_exists(user):
    assert user("postgres").exists
    assert user("postgres").shell == "/usr/sbin/nologin"


def test_postgres_group_exists(group):
    assert group("postgres").exists


def test_postgres_config_directory_permissions(file):
    postgres_cfg_dir = file("/etc/postgresql")
    assert postgres_cfg_dir.exists
    assert postgres_cfg_dir.is_directory
    assert postgres_cfg_dir.user == "postgres"
    assert postgres_cfg_dir.group == "postgres"
    assert oct(postgres_cfg_dir.mode) == "0o755"


def test_postgres_storage_directory_permissions(file):
    postgres_storage_dir = file("/var/lib/postgresql")
    assert postgres_storage_dir.exists
    assert postgres_storage_dir.is_directory
    assert postgres_storage_dir.user == "postgres"
    assert postgres_storage_dir.group == "postgres"
    assert oct(postgres_storage_dir.mode) == "0o755"


def test_psql_command_is_availablie(host):
    assert host.exists("psql")


def test_postgres_processes_are_running_as_postgres(process):
    for p in process("postgres"):
        print(p)
        assert p.user == "postgres"
        assert p.group == "postgres"


def test_postgres_is_listening(socket):
    postgres = "tcp://0.0.0.0:5432"
    assert socket(postgres).is_listening


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
        return host.process.filter(comm=process_name)
    return _func


@pytest.fixture()
def socket(host):
    def _func(spec):
        return host.socket(spec)
    return _func
