import json
import pytest
import write_log

import ansible.module_utils.basic as ansible_utils
import unittest.mock as mock


MODULE_NAME = "write_log"


def test_present_dir_does_not_exist(set_fake_module):
    args = dict(
        name="test",
        message="test message",
        state="present",
        dir="./does-not-exist",
    )
    set_fake_module(args, _fake_exit_json)

    # when
    with pytest.raises(FileNotFoundError) as exc_info:
        _ = write_log.run()

    # then
    assert exc_info.type is FileNotFoundError, (
        "should rise FileNotFoundError when the state is present the dir does not exist"
    )


def test_present_file_does_not_exist(set_fake_module):
    args = dict(
        name="test",
        message="test messsage",
        state="present",
        dir="/tmp",
    )
    set_fake_module(args, _fake_exit_json)
    log_file = f"{args['dir']}/{args['name']}"

    # when
    with (
        pytest.raises(ExitJsonError) as exc_info,
        mock.patch(f"{MODULE_NAME}.os.path.exists", _os_path_not_exist()) as mock_os_path_exists,
        mock.patch(f"{MODULE_NAME}.open", mock.mock_open()) as mock_open,
    ):
        _ = write_log.run()

    # then
    mock_os_path_exists.assert_called_with(log_file)
    mock_open.assert_called_once_with(log_file, mode="w", encoding="utf-8")
    assert _module_results(exc_info)["changed"] is True, (
        "should be changed when the state is present the file does not exist"
    )


def test_present_file_exists_different_contents(set_fake_module):
    args = dict(
        name="test",
        message="test messsage",
        state="present",
        dir="/tmp",
    )
    set_fake_module(args, _fake_exit_json)
    log_file = f"{args['dir']}/{args['name']}"

    # when
    with (
        pytest.raises(ExitJsonError) as exc_info,
        mock.patch(f"{MODULE_NAME}.os.path.exists", _os_path_exists()) as mock_os_path_exists,
        mock.patch(f"{MODULE_NAME}.open", mock.mock_open(read_data="data")) as mock_open,
    ):
        _ = write_log.run()

    # then
    mock_os_path_exists.assert_called_with(log_file)
    mock_open.assert_called_with(log_file, mode="w", encoding="utf-8")
    assert _module_results(exc_info)["changed"] is True, (
        "should be changed when the state is present the file contents is different"
    )


def test_present_file_exists_same_contents(set_fake_module):
    args = dict(
        name="test",
        message="test messsage",
        state="present",
        dir="/tmp",
    )
    set_fake_module(args, _fake_exit_json)
    log_file = f"{args['dir']}/{args['name']}"
    log_message = f"{args['name']}: {args['message']}\n"

    # when
    with (
        pytest.raises(ExitJsonError) as exc_info,
        mock.patch(f"{MODULE_NAME}.os.path.exists", _os_path_exists()) as mock_os_path_exists,
        mock.patch(f"{MODULE_NAME}.open", mock.mock_open(read_data=log_message)) as mock_open,
    ):
        _ = write_log.run()

    # then
    mock_os_path_exists.assert_called_with(log_file)
    mock_open.assert_called_with(log_file, mode="w", encoding="utf-8")
    assert _module_results(exc_info)["changed"] is False, (
        "should not be changed when the state is present and the file contents is the same"
    )


def test_check_mode_enabled_state_present(set_fake_module):
    args = dict(
        name="test",
        message="test messsage",
        state="present",
        dir="/tmp",
        _ansible_check_mode=True,
    )
    set_fake_module(args, _fake_exit_json)

    # when
    with (
        pytest.raises(ExitJsonError) as exc_info,
        mock.patch(f"{MODULE_NAME}.os.path.exists", _os_path_exists()) as mock_os_path_exists,
        mock.patch(f"{MODULE_NAME}.open", mock.mock_open()) as mock_open,
    ):
        _ = write_log.run()

    # then
    mock_os_path_exists.assert_not_called()
    mock_open.assert_not_called()
    assert _module_results(exc_info)["changed"] is False, (
        "should not be changed when the state is present and check mode is enabled"
    )


def test_check_mode_enabled_state_absent(set_fake_module):
    args = dict(
        name="test",
        message="test messsage",
        state="absent",
        dir="/tmp",
        _ansible_check_mode=True,
    )
    set_fake_module(args, _fake_exit_json)

    # when
    with (
        pytest.raises(ExitJsonError) as exc_info,
        mock.patch(f"{MODULE_NAME}.os.path.exists", _os_path_exists()) as mock_os_path_exists,
        mock.patch(f"{MODULE_NAME}.open", mock.mock_open()) as mock_open,
        mock.patch(f"{MODULE_NAME}.os.remove", _os_remove()) as mock_os_remove,
    ):
        _ = write_log.run()

    # then
    mock_os_path_exists.assert_not_called()
    mock_open.assert_not_called()
    mock_os_remove.assert_not_called()
    assert _module_results(exc_info)["changed"] is False, (
        "should not be changed when the state is absent and check mode is enabled"
    )


def test_absent_dir_does_not_exist(set_fake_module):
    args = dict(
        name="test",
        message="test message",
        state="absent",
        dir="./does-not-exist",
    )
    set_fake_module(args, _fake_exit_json)

    # when
    with pytest.raises(ExitJsonError) as exc_info:
        _ = write_log.run()

    # then
    assert _module_results(exc_info)["changed"] is False, (
        "should not be changed when the state is absent and the dir does not exist"
    )


def test_absent_file_exists(set_fake_module):
    args = dict(
        name="test",
        message="test messsage",
        state="absent",
        dir="/tmp",
    )
    set_fake_module(args, _fake_exit_json)
    log_file = f"{args['dir']}/{args['name']}"

    # when
    with (
        pytest.raises(ExitJsonError) as exc_info,
        mock.patch(f"{MODULE_NAME}.os.path.exists", _os_path_exists()) as mock_os_path_exists,
        mock.patch(f"{MODULE_NAME}.os.remove", _os_remove()) as mock_os_remove,
    ):
        _ = write_log.run()

    # then
    mock_os_path_exists.assert_called_with(log_file)
    mock_os_remove.assert_called_once_with(log_file)
    assert _module_results(exc_info)["changed"] is True, (
        "should be changed when state is absent and the file exists"
    )


def test_absent_file_does_not_exist(set_fake_module):
    args = dict(
        name="test",
        message="test messsage",
        state="absent",
        dir="/tmp",
    )
    set_fake_module(args, _fake_exit_json)
    log_file = f"{args['dir']}/{args['name']}"

    # when
    with (
        pytest.raises(ExitJsonError) as exc_info,
        mock.patch(f"{MODULE_NAME}.os.path.exists", _os_path_not_exist()) as mock_os_path_exists,
        mock.patch(f"{MODULE_NAME}.os.remove", _os_remove()) as mock_os_remove,
    ):
        _ = write_log.run()

    # then
    mock_os_path_exists.assert_called_with(log_file)
    mock_os_remove.assert_not_called()
    assert _module_results(exc_info)["changed"] is False, (
        "should not be changed when state is absent and the file does not exist"
    )


@pytest.fixture()
def set_fake_module(monkeypatch):
    def _func(args, exit_json):
        overwrite_args = {
            "_ansible_remote_tmp": "/tmp",
            "_ansible_keep_remote_files": False,
        }

        module_args = args | overwrite_args  # merge dicts
        args = json.dumps({"ANSIBLE_MODULE_ARGS": module_args})
        ansible_utils._ANSIBLE_ARGS = ansible_utils.to_bytes(args)

        monkeypatch.setattr(f"{MODULE_NAME}.AnsibleModule.exit_json", exit_json)
    return _func


class ExitJsonError(Exception):
    pass


def _module_results(exc_info):
    return exc_info.value.args[0]


def _fake_exit_json(*args, **kwargs):
    if 'changed' not in kwargs:
        kwargs['changed'] = False
    raise ExitJsonError(kwargs)


def _os_path_exists(*args):
    return mock.MagicMock(return_value=True)


def _os_path_not_exist(*args):
    return mock.MagicMock(return_value=False)


def _os_remove(*args):
    return mock.MagicMock()
