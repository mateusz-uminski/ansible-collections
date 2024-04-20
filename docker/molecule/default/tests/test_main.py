import pytest


def test_docker_is_running(service):
    assert service("docker").is_running


def test_containerd_is_running(service):
    assert service("containerd").is_running


def test_docker_is_enabled(service):
    assert service("docker").is_enabled


def test_containerd_is_enabled(service):
    assert service("containerd").is_enabled


def test_docker_is_running_as_root(process):
    process_name = "dockerd"
    assert process(process_name).user == "root"
    assert process(process_name).group == "root"


def test_containerd_is_running_as_root(process):
    process_name = "containerd"
    assert process(process_name).user == "root"
    assert process(process_name).group == "root"


def test_docker_group_exists(group):
    assert group("docker").exists


@pytest.fixture()
def service(host):
    def _func(service_name):
        return host.service(service_name)
    return _func


@pytest.fixture()
def process(host):
    def _func(process_name):
        return host.process.get(comm=process_name)
    return _func


@pytest.fixture()
def group(host):
    def _func(group_name):
        return host.group(group_name)
    return _func
