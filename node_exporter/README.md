# node_exporter

Ansible collection that installs node-exporter.

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
    - name: install node exporter
      ansible.builtin.import_role:
        name: infra.node_exporter.install
      vars:
        node_exporter_version: 1.8.2
        node_exporter_ip_addr: 0.0.0.0
        node_exporter_port: 9100
```
