# haproxy

Ansible collection that installs haproxy.

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
    haproxy_config:
      - name: example
        frontend: |-
          bind    *:80
          mode    tcp
          option  tcplog
        backend: |-
          balance first
          server worker1 10.0.0.1:30080 id 10
          server worker2 10.0.0.2:30080 id 20
          server worker3 10.0.0.2:30080 id 30
    haproxy_stats:
      enabled: true
      port: 9090
      refresh: 10s
  tasks:
    - name: install haproxy
      ansible.builtin.import_role:
        name: infra.haproxy.install
```
