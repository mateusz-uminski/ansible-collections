def test_file_exists(host):
    assert host.file("/tmp/admin").exists
