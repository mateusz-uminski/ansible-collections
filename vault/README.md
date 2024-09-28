# vault

Ansible collection that installs vault in server mode. The collection supports high availability deployment.

# Compatibility
The collection was tested on the following platforms:
- Debian 12 (x86 & aarch64)
- AlmaLinux 9 (x86 & aarch64)
- Amazon Linux 2023 (x86 & aarch64)

# Usage

```yaml
- name: example
  hosts: vault  # a group of size N requires at least (N/2)+1 hosts in the group to form a quorum.
  gather_facts: true
  tasks:
    - name: install vault server
      ansible.builtin.import_role:
        name: infra.vault.install
      vars:
        vault_version: 1.17.6-1
        vault_cluster_name: cluster
        vault_secret_shares: 5
        vault_secret_threshold: 3
```
