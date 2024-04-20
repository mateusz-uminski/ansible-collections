import pytest


def test_service_is_running(service):
    assert service("haproxy").is_running


def test_service_is_enabled(service):
    assert service("haproxy").is_enabled


def test_haproxy_user_exists(user):
    assert user("haproxy").exists
    assert user("haproxy").shell == "/usr/sbin/nologin"


def test_haproxy_group_exists(group):
    assert group("haproxy").exists


def test_haproxy_config_permissions(file):
    haproxy_cfg = file("/etc/haproxy/haproxy.cfg")
    assert haproxy_cfg.exists
    assert haproxy_cfg.user == "haproxy"
    assert haproxy_cfg.group == "haproxy"
    assert oct(haproxy_cfg.mode) == "0o644"


def test_haproxy_main_process_is_running_as_root(process):
    process_name = "haproxy"
    assert process("root", process_name).user == "root"
    assert process("root", process_name).group == "root"


def test_haproxy_fork_processes_are_running_as_haproxy(process, forks):
    haproxy_proc = process("root", "haproxy")

    workers = forks(haproxy_proc.pid)
    for w in workers:
        assert w.user == "haproxy"
        assert w.group == "haproxy"


def test_haproxy_is_listening_on_ports(socket):
    example_frontend_from_defaults = "tcp://0.0.0.0:80"
    assert socket(example_frontend_from_defaults).is_listening
    haproxy_stats = "tcp://0.0.0.0:9090"
    assert socket(haproxy_stats).is_listening


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
    def _func(user, process_name):
        return host.process.get(user=user, comm=process_name)
    return _func


@pytest.fixture()
def forks(host):
    def _func(pid):
        return host.process.filter(ppid=pid)
    return _func


@pytest.fixture()
def socket(host):
    def _func(spec):
        return host.socket(spec)
    return _func
