# nexus

Ansible collection that installs nexus.

# Compatibility
The collection was tested on the following platforms:
- Debian 12 (x86)
- AlmaLinux 9 (x86)
- Amazon Linux 2023 (x86)

# Usage

```yaml
- name: example
  hosts: all
  gather_facts: true
  tasks:
    - name: install nexus
      ansible.builtin.import_role:
        name: infra.nexus.install
      vars:
        nexus_version: 3.72.0-04
```
