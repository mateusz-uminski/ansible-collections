# iptables

Ansible collection that configures iptables rules.

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
    - name: configure iptables
      ansible.builtin.import_role:
        name: infra.iptables.configure
      vars:
        iptables_conf_dir: /etc/iptables
        iptables_flush_all_rules: true
        iptables_debug: false
        iptables_log_dropped_packets: true
        iptables_log_rate_limit: 5/min
        iptables_allowed_tcp_ports:
          - 22
        iptables_custom_rules:
          - "iptables -A INPUT -s 203.0.113.51 -j DROP"
```
