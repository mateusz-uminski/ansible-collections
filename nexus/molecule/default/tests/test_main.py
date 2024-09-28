import pytest


def test_service_is_running(service):
    assert service("nexus").is_running


def test_service_is_enabled(service):
    assert service("nexus").is_enabled


def test_nexus_user_exists(user):
    assert user("nexus").exists
    assert user("nexus").shell == "/usr/sbin/nologin"


def test_nexus_group_exists(group):
    assert group("nexus").exists


def test_nexus_directory_permissions(file):
    nexus_dir = file("/opt/nexus-3.72.0-04/")
    assert nexus_dir.exists
    assert nexus_dir.is_directory
    assert nexus_dir.user == "nexus"
    assert nexus_dir.group == "nexus"
    assert oct(nexus_dir.mode) == "0o755"


def test_sonatype_work_directory_permissions(file):
    sonatype_work_dir = file("/opt/sonatype-work/")
    assert sonatype_work_dir.exists
    assert sonatype_work_dir.is_directory
    assert sonatype_work_dir.user == "nexus"
    assert sonatype_work_dir.group == "nexus"
    assert oct(sonatype_work_dir.mode) == "0o755"


def test_nexus_is_running_as_nexus(process):
    process_name = "java"
    assert process(process_name).user == "nexus"
    assert process(process_name).group == "nexus"


def test_nexus_is_listening(socket):
    nexus = "tcp://0.0.0.0:8081"
    assert socket(nexus).is_listening


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
