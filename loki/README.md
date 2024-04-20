# loki

Ansible collection that installs loki. The collection supports deployment using a local file system or AWS S3 as storage.

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
  vars:
    loki_config_dir: /etc/loki
    loki_storage_dir: /var/lib/loki
    loki_enable_auth: false
    loki_log_level: info
    loki_storage: filesystem
    loki_storage_conf:
      filesystem:
        ring_kv_store: inmemory
        tsdb_object_store: filesystem
  tasks:
    - name: install loki
      ansible.builtin.import_role:
        name: infra.loki.install
```

## aws s3 storage
```yaml
- name: s3
  hosts: all
  gather_facts: true
  vars:
    loki_config_dir: /etc/loki
    loki_storage_dir: /var/lib/loki
    loki_enable_auth: false
    loki_log_level: info
    loki_storage: s3
    loki_storage_conf:
      s3:
        ring_kv_store: inmemory
        endpoint: https://s3.console.aws.amazon.com/
        bucketnames: bucketname
        region: us-east-1
        insecure: false
        sse_encryption: false
        tsdb_object_store: aws
  tasks:
    - name: install loki
      ansible.builtin.import_role:
        name: infra.loki.install
```
