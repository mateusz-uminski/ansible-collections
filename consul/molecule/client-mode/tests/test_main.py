import pytest


def test_service_is_running(service):
    assert service("consul").is_running


def test_service_is_enabled(service):
    assert service("consul").is_enabled


def test_consul_user_exists(user):
    assert user("consul").exists
    assert user("consul").shell == "/bin/false"


def test_consul_group_exists(group):
    assert group("consul").exists


def test_consul_config_permissions(file):
    consul_cfg = file("/etc/consul.d/consul.hcl")
    assert consul_cfg.exists
    assert consul_cfg.user == "consul"
    assert consul_cfg.group == "consul"
    assert oct(consul_cfg.mode) == "0o644"


def test_consul_is_running_as_consul(process):
    process_name = "consul"
    assert process(process_name).user == "consul"
    assert process(process_name).group == "consul"


def test_consul_command_is_availablie(host):
    assert host.exists("consul")


def test_consul_number_of_members_in_client_mode(host):
    num_servers = int(host.run("consul members | grep client | wc -l").stdout)
    assert num_servers == 1


def test_consul_is_listening_on_ports(default_addr, socket):
    sockets = {
        'consul_ui_http': "tcp://0.0.0.0:8500",
        # 'consul_ui_https': "tcp://0.0.0.0:8501",
        'consul_dns': "tcp://0.0.0.0:8600",
        'consul_lan_serf': f"tcp://{default_addr()}:8301",
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


@pytest.fixture()
def default_addr(host):
    def _func():
        return host.interface.default().addresses[0]
    return _func
