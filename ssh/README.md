# ssh

Ansible collection that installs sshd and configures ssh authorized keys on servers.

# Compatibility
The collection was tested on the following platforms:
- Debian 12 (x86 & aarch64)
- AlmaLinux 9 (x86 & aarch64)
- Amazon Linux 2023 (x86 & aarch64)

# Usage

## Install sshd
```yaml
- name: example
  hosts: all
  gather_facts: true
  tasks:
    - name: install ssh
      ansible.builtin.import_role:
        name: infra.ssh.install
      vars:
        ssh_authorized_keys_fallback_dir: /etc/ssh/authorized_keys
        ssh_port: 22
        ssh_permit_root_login: without-password
        ssh_password_authentication: "no"
        ssh_permit_empty_password: "no"
        ssh_use_pam: "no"
        ssh_x11_forwarding: "no"
```

## Configure authorized keys

```yaml
- name: example
  hosts: all
  gather_facts: true
  tasks:
    - name: configure authorized keys
      ansible.builtin.import_role:
        name: infra.ssh.pubkeys
      vars:
        ssh_authorized_keys:
          - remote_user: root
            allowed_pubkeys: |
              ssh-rsa notsolongpubkeyvalue1== user1@example.com
              ssh-rsa notsolongpubkeyvalue2== user2@example.com
```
