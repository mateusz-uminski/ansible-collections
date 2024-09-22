# tempo

Ansible collection that installs tempo. The collection supports deployment using a local file system or AWS S3 as storage.

# Compatibility
The collection was tested on the following platforms:
- Debian 12 (x86 & aarch64)
- AlmaLinux 9 (x86 & aarch64)
- Amazon Linux 2023 (x86 & aarch64)

# Usage

## filesystem storage
```yaml
- name: filesystem
  hosts: all
  gather_facts: true
  tasks:
    - name: install tempo
      ansible.builtin.import_role:
        name: infra.tempo.install
      vars:
        tempo_config_dir: /etc/tempo
        tempo_storage_backend: local
        tempo_storage_dir: /tmp/tempo
        tempo_metrics_remote_write: http://prometheus:9090/api/v1/write
        tempo_metrics_labels:
          source: tempo
```

## aws s3 storage
```yaml
- name: s3
  hosts: all
  gather_facts: true
  tasks:
    - name: install tempo
      ansible.builtin.import_role:
        name: infra.tempo.install
      vars:
          tempo_config_dir: /etc/tempo
          tempo_storage_backend: s3
          tempo_storage_dir: /tmp/tempo
          tempo_s3_storage_bucket_name: <bucket_name>
          tempo_log_level: info
          tempo_metrics_remote_write: http://prometheus:9090/api/v1/write
          tempo_metrics_labels:
            source: tempo
```
