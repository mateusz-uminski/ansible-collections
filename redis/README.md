# redis

Ansible collection that installs redis server.

# Compatibility
The collection was tested on the following platforms:
- Debian 12 (x86 & aarch64)
- AlmaLinux 9 (x86 & aarch64)

# Usage

```yaml
- name: example
  hosts: all
  gather_facts: true
  tasks:
    - name: install redis server
      ansible.builtin.import_role:
        name: infra.redis.install
      vars:
        redis_ip_addr: 0.0.0.0
        redis_port: 6379
        redis_timeout: 300
        redis_conf_dir: /etc/redis
        redis_loglevel: debug
        redis_log_dir: /var/log/redis
        redis_db_dir: /var/lib/redis
        redis_databases: 16
        redis_save:
          - 3600 1
          - 300 100
          - 60 10000
        redis_maxmemory: 10mb
        redis_maxmemory_policy: noeviction
        redis_maxmemory_samples: 5
        redis_appendonly: "yes"
        redis_appendfsync: everysec
        redis_disabled_commands: []
```
