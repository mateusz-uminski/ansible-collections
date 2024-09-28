import pytest


def test_is_service_running(service):
    assert service("nginx").is_running


def test_is_service_enabled(service):
    assert service("nginx").is_enabled


def test_nginx_user_exists(distribution, user):
    nologin_shell = "/usr/sbin/nologin"
    if distribution() != "debian":
        nologin_shell = "/sbin/nologin"

    assert user("nginx").exists
    assert user("nginx").shell == nologin_shell


def test_nginx_group_exists(group):
    assert group("nginx").exists


def test_nginx_config_file_permissions(file):
    nginx_cfg_file = file("etc/nginx/nginx.conf")
    assert nginx_cfg_file.exists
    assert nginx_cfg_file.is_file
    assert nginx_cfg_file.user == "nginx"
    assert nginx_cfg_file.group == "nginx"
    assert oct(nginx_cfg_file.mode) == "0o644"


def test_nginx_vhost_file_permissions(file):
    nginx_vhost_file = file("etc/nginx/conf.d/vhost.conf")
    assert nginx_vhost_file.exists
    assert nginx_vhost_file.is_file
    assert nginx_vhost_file.user == "nginx"
    assert nginx_vhost_file.group == "nginx"
    assert oct(nginx_vhost_file.mode) == "0o644"


def test_nginx_main_process_is_running_as_root(process):
    process_name = "nginx"
    assert process("root", process_name).user == "root"
    assert process("root", process_name).group == "root"


def test_nginx_fork_processes_are_running_as_nginx(process, forks):
    nginx_proc = process("root", "nginx")

    workers = forks(nginx_proc.pid)
    for w in workers:
        assert w.user == "nginx"
        assert w.group == "nginx"


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
