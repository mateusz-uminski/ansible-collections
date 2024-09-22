# postgres

Ansible collection that installs postgresql.

# Compatibility
The collection was tested on the following platforms:
- Debian 12 (x86 & aarch64)

# Usage

```yaml
- name: example
  hosts: all
  gather_facts: true
  tasks:
    - name: install postgres
      ansible.builtin.import_role:
        name: infra.postgres.install
      vars:
        postgres_version: 15
        postgres_pg_hba_entries:
          - host all all 0.0.0.0/0 md5
```
