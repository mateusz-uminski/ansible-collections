# nginx

Ansible collection that installs nginx.

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
  tasks:
    - name: install nginx
      ansible.builtin.import_role:
        name: infra.nginx.install
      vars:
        nginx_vhost_servers:
          - id: example_server
            listen: 80
            server_name: default
            access_log_level: main
            error_log_level: error
            locations:
              - path: /
                type: application/json
                return: 200 '{"status":"success","message":"hello world"}'
              - path: /ping
                type: application/json
                return: 200 '{"status":"success","message":"pong"}'

```
