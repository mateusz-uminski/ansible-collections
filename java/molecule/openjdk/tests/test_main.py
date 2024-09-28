def test_java_is_installed(host):
    rc = host.run("java --version").rc
    assert rc == 0


def test_java_home_is_set(host):
    java_home = host.run("dirname $(dirname $(readlink -f /etc/alternatives/java))").stdout.strip()
    env_stdout = host.run("/bin/bash -c 'source /etc/profile.d/java.sh && env'").stdout
    assert java_home == _env_dict(env_stdout)["JAVA_HOME"]


def _env_dict(output):
    env = {}
    lines = output.strip().split('\n')
    for l in lines:  # noqa E741
        k, v = l.split('=', 1)
        env[k] = v.strip()
    return env
