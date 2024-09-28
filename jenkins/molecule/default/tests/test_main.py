import pytest


def test_service_is_running(service):
    assert service("jenkins").is_running


def test_service_is_enabled(service):
    assert service("jenkins").is_enabled


def test_jenkins_user_exists(user):
    assert user("jenkins").exists
    assert user("jenkins").shell == "/usr/sbin/nologin"


def test_jenkins_group_exists(group):
    assert group("jenkins").exists


def test_jenkins_home_directory_permissions(file):
    jenkins_home_dir = file("/var/lib/jenkins")
    assert jenkins_home_dir.exists
    assert jenkins_home_dir.is_directory
    assert jenkins_home_dir.user == "jenkins"
    assert jenkins_home_dir.group == "jenkins"
    assert oct(jenkins_home_dir.mode) == "0o755"


def test_jenkins_working_directory_permissions(file):
    jenkins_working_dir = file("/var/lib/jenkins")
    assert jenkins_working_dir.exists
    assert jenkins_working_dir.is_directory
    assert jenkins_working_dir.user == "jenkins"
    assert jenkins_working_dir.group == "jenkins"
    assert oct(jenkins_working_dir.mode) == "0o755"


def test_jenkins_is_running_as_jenkins(process):
    process_name = "java"
    assert process(process_name).user == "jenkins"
    assert process(process_name).group == "jenkins"


def test_jenkins_is_listening(socket):
    jenkins = "tcp://0.0.0.0:8080"
    assert socket(jenkins).is_listening


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
