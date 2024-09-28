# java

Ansible collection that installs java.

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
    - name: install openjdk
      ansible.builtin.import_role:
        name: infra.java.openjdk
      vars:
        java_openjdk_version: 17
```
