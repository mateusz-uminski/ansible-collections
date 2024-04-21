# experimental

Ansible collection that shows how to write custom plugins. For now, the collection contains only one plugin called `write_log`.


# Compatibility

The collection was tested on the following platforms:
- Debian 12 (x86 & aarch64)
- AlmaLinux 9 (x86 & aarch64)
- Amazon Linux 2023 (x86 & aarch64)


# Usage

```yaml
- name: example
  hosts: all
  gather_facts: true
  vars:
    experimental_name: admin
    experimental_message: hello!
  tasks:
    - name: run a role from the collection
      ansible.builtin.import_role:
        name: infra.experimental.run
```


# Plugins

## Development

1. Configure environment:
```sh
cd $(git rev-parse --show-toplevel)
python3 -m venv venv/
source venv/bin/activate
pip install pip --upgrade
pip install -r requirements.txt
```

2. Execute unit tests:
```sh
cd $(git rev-parse --show-toplevel)
pytest experimental/plugins/
```

3. Execute a custom module plugin using an ad hoc command:
```sh
cd $(git rev-parse --show-toplevel)
ANSIBLE_LIBRARY=experimental/plugins/ ansible -m write_log -a 'name=experimental message=hello! state=present' localhost
```


## modules/write_log

The plugin writes a given message to a file in the specified directory when the state is `present` and deletes the specified file when the state is `absent`. If the file exists, the plugin overwrites its contents.
The `check_mode` is supported by the `write_log`.


### Usage

#### inside the collection
```yaml
- name: run a custom module
  write_msg:
    name: "{{ experimental_name }}"
    message: "{{ experimental_message }}"
    dir: /tmp
    state: present
```


#### outside the collection
```yaml
- name: run a custom module
  infra.experimental.write_log:
    name: "{{ experimental_name }}"
    message: "{{ experimental_message }}"
    dir: /tmp
    state: present
```
