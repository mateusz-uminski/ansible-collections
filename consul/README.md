# consul

Ansible collection that installs consul in either server or client mode. The collection supports high availability deployment of consul in server mode.

# Compatibility
The collection was tested on the following platforms:
- Debian 12 (x86 & aarch64)
- AlmaLinux 9 (x86 & aarch64)
- Amazon Linux 2023 (x86 & aarch64)


# Prerequisites
1. Generate a consul key:
```sh
docker run -it --rm hashicorp/consul consul keygen
```
2. Use the command output to set the `consul_key` variable.


# Usage

## server mode
```yaml
- name: server mode
  hosts: controlplane  # a group of size N requires at least (N/2)+1 hosts in the group to form a quorum.
  gather_facts: true
  vars:
    consul_key: qDOPBEr+/oUVeOFQOnVypxwDaHzLrD+lvjo5vCEBbZ0=
    consul_server_mode: true
    consul_servers: []
    consul_dc_name: "dc1"
    consul_domain: "consul"
    consul_log_level: "INFO"
    consul_enable_acl: false
    consul_raft_multiplier: 1
  tasks:
    - name: install consul server
      ansible.builtin.import_role:
        name: infra.consul.install
```

## client mode
```yaml
- name: client mode
  hosts: clients
  gather_facts: true
  vars:
    consul_key: qDOPBEr+/oUVeOFQOnVypxwDaHzLrD+lvjo5vCEBbZ0=
    consul_server_mode: false
    consul_servers: ["server:8301"]
    consul_dc_name: "dc1"
    consul_domain: "consul"
    consul_log_level: "INFO"
  tasks:
    - name: install consul client
      ansible.builtin.import_role:
        name: infra.consul.install
```
