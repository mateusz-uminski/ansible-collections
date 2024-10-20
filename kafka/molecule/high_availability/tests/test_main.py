import pytest


def test_service_is_running(service):
    assert service("kafka").is_running


def test_service_is_enabled(service):
    assert service("kafka").is_enabled


def test_kafka_user_exists(user):
    assert user("kafka").exists
    assert user("kafka").shell == "/usr/sbin/nologin"


def test_kafka_group_exists(group):
    assert group("kafka").exists


def test_kafka_directory_permissions(file):
    kafka_dir = file("/opt/kafka-2.13-3.8.0")
    assert kafka_dir.exists
    assert kafka_dir.is_directory
    assert kafka_dir.user == "kafka"
    assert kafka_dir.group == "kafka"
    assert oct(kafka_dir.mode) == "0o755"


def test_kafka_data_directory_permissions(file):
    kafka_data_dir = file("/var/lib/kafka/data")
    assert kafka_data_dir.exists
    assert kafka_data_dir.is_directory
    assert kafka_data_dir.user == "kafka"
    assert kafka_data_dir.group == "kafka"
    assert oct(kafka_data_dir.mode) == "0o755"


def test_kafka_storage_is_formatted(file):
    kafka_data_dir = file("/var/lib/kafka/data/meta.properties")
    assert kafka_data_dir.exists
    assert kafka_data_dir.is_file
    assert kafka_data_dir.user == "kafka"
    assert kafka_data_dir.group == "kafka"
    assert oct(kafka_data_dir.mode) == "0o644"


def test_kafka_is_running_as_kafka(process):
    process_name = "java"
    assert process(process_name).user == "kafka"
    assert process(process_name).group == "kafka"


def test_kafka_is_listening(socket):
    kafka = "tcp://0.0.0.0:9093"
    assert socket(kafka).is_listening


def test_kafka_current_voters(host):
    kafka_home_dir = "/opt/kafka-2.13-3.8.0"
    kafka_script = "./bin/kafka-metadata-quorum.sh"
    kafka_script_args = "--bootstrap-controller localhost:9093 describe --status"

    get_voters_cmd = f"{kafka_home_dir}/{kafka_script} {kafka_script_args}"
    grep_cmd = "grep CurrentVoters"
    sed_cmd = "sed 's/CurrentVoters:[[:space:]]*//'"

    # when
    current_voters = host.run(f"{get_voters_cmd} | {grep_cmd} | {sed_cmd}").stdout

    # then
    assert current_voters == "[1,2,3]\n"


def test_kafka_current_observers(host):
    kafka_home_dir = "/opt/kafka-2.13-3.8.0"
    kafka_script = "./bin/kafka-metadata-quorum.sh"
    kafka_script_args = "--bootstrap-controller localhost:9093 describe --status"

    get_observers_cmd = f"{kafka_home_dir}/{kafka_script} {kafka_script_args}"
    grep_cmd = "grep CurrentObservers"
    sed_cmd = "sed 's/CurrentObservers:[[:space:]]*//'"

    # when
    current_observers = host.run(f"{get_observers_cmd} | {grep_cmd} | {sed_cmd}").stdout

    # then
    assert current_observers == "[]\n"


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
