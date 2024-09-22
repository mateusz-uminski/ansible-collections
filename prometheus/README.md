# prometheus

Ansible collection that installs prometheus server.

# Compatibility
The collection was tested on the following platforms:
- Debian 12 (x86 & aarch64)
- AlmaLinux 9 (x86 & aarch64)
- Amazon Linux 2023 (x86 & aarch64)

# Usage

```yaml
- name: filesystem
  hosts: all
  gather_facts: true
  tasks:
    - name: install prometheus server
      ansible.builtin.import_role:
        name: infra.prometheus.install
      vars:
        prometheus_version: 2.54.0
        prometheus_conf_dir: /etc/prometheus
        prometheus_db_dir: /var/lib/prometheus
        prometheus_data_retention: 30d
        prometheus_external_labels:
          environment: sandbox
        prometheus_global:
          scrape_interval: 1m
          scrape_timeout: 30s
          evaluation_interval: 1m
        prometheus_remote_write: []
        prometheus_remote_read: []
        prometheus_scrape_configs: []
```
