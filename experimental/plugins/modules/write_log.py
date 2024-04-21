import os

from ansible.module_utils.basic import AnsibleModule


def check_mode(log_file, log_message):
    result = {
        "changed": False,
        "log": log_message,
        "path": log_file,
    }
    return result


def present(log_file, log_message):
    result = {
        "changed": False,
        "log": log_message,
        "path": log_file,
    }

    if os.path.exists(log_file):
        with open(log_file, mode="r", encoding="utf-8") as f:
            if log_message != f.read():
                result["changed"] = True

    if not os.path.exists(log_file):
        result["changed"] = True

    with open(log_file, mode="w", encoding="utf-8") as f:
        f.write(log_message)

    return result


def absent(log_file):
    result = {
        "changed": False,
        "path": log_file,
    }

    if not os.path.exists(log_file):
        return result

    if os.path.exists(log_file):
        result["changed"] = True
        os.remove(log_file)

    return result


def run():
    argument_spec = dict(
        name=dict(required=True, type="str"),
        message=dict(required=True, type="str"),
        dir=dict(required=False, type="str", default="/tmp"),
        state=dict(required=True, type="str", choices=["present", "absent"]),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    name = module.params["name"]
    message = module.params["message"]
    dir = module.params["dir"]
    state = module.params["state"]
    log_file = f"{dir}/{name}"
    log_message = f"{name}: {message}\n"

    if module.check_mode:
        result = check_mode(log_file, log_message)
        return module.exit_json(**result)

    if state == "present":
        result = present(log_file, log_message)
    elif state == "absent":
        result = absent(log_file)

    return module.exit_json(**result)


if __name__ == '__main__':
    run()
