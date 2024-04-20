# admin

Ansible collection that configures the admin environment.


# Compatibility
The collection was tested on the following platforms:
- Debian 12 (x86 & aarch64)
- AlmaLinux 9 (x86 & aarch64)
- Amazon Linux 2023 (x86 & aarch64)


# Usage

## role: install
```yaml
- name: example
  hosts: all
  gather_facts: true
  tasks:
    - name: configure admin environment
      ansible.builtin.import_role:
        name: infra.admin.install
```
