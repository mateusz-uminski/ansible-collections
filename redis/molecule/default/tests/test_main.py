import pytest


def test_service_is_running(service):
    assert service("redis").is_running


def test_service_is_enabled(service):
    assert service("redis").is_enabled


def test_redis_user_exists(user):
    assert user("redis").exists
    assert user("redis").shell == "/bin/nologin"


def test_redis_group_exists(group):
    assert group("redis").exists


def test_redis_config_directory_permissions(file):
    redis_cfg_dir = file("/etc/redis")
    assert redis_cfg_dir.exists
    assert redis_cfg_dir.is_directory
    assert redis_cfg_dir.user == "redis"
    assert redis_cfg_dir.group == "redis"
    assert oct(redis_cfg_dir.mode) == "0o755"


def test_redis_log_directory_permissions(file):
    redis_cfg_dir = file("/var/log/redis")
    assert redis_cfg_dir.exists
    assert redis_cfg_dir.is_directory
    assert redis_cfg_dir.user == "redis"
    assert redis_cfg_dir.group == "redis"
    assert oct(redis_cfg_dir.mode) == "0o750"


def test_redis_storage_directory_permissions(file):
    redis_storage_dir = file("/var/lib/redis")
    assert redis_storage_dir.exists
    assert redis_storage_dir.is_directory
    assert redis_storage_dir.user == "redis"
    assert redis_storage_dir.group == "redis"
    assert oct(redis_storage_dir.mode) == "0o750"


def test_redis_config_permissions(file):
    redis_cfg = file("/etc/redis/redis.conf")
    assert redis_cfg.exists
    assert redis_cfg.user == "redis"
    assert redis_cfg.group == "redis"
    assert oct(redis_cfg.mode) == "0o644"


def test_redis_is_running_as_redis(process):
    process_name = "redis-server"
    assert process(process_name).user == "redis"
    assert process(process_name).group == "redis"


def test_redis_is_listening(socket):
    redis = "tcp://0.0.0.0:6379"
    assert socket(redis).is_listening


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
    # ps -A -o comm
    def _func(process_name):
        return host.process.get(comm=process_name)
    return _func


@pytest.fixture()
def socket(host):
    def _func(spec):
        return host.socket(spec)
    return _func
