# kafka

Ansible collection that automates the setup of Apache Kafka in Kraft mode, with optional high availability (HA) configuration. It includes the following roles:
- **install**: installs kafka kraft controllers, optionally configures controllers in HA mode, or installs brokers and connect them to a given Kafka cluster.
- **akhq**: Installs AKHQ and connects it to a specified Kafka cluster for management and monitoring.


# Compatibility
The collection was tested on the following platforms:
- Debian 12 (x86)
- AlmaLinux 9 (x86)
- Amazon Linux 2023 (x86)


# Usage

## controller
```yaml
- name: controlplane
  hosts: all
  gather_facts: true
  tasks:
    - name: install kafka controller
      ansible.builtin.import_role:
        name: infra.kafka.install
      vars:
        kafka_version: 3.8.0
        kafka_scala_version: 2.13
        kafka_role: controller
        kafka_data_dir: "/var/lib/kafka/data"
        kafka_cluster_id: "XeBwhcj6SfiR_07KLddO-w"
```


## broker
```yaml
- name: brokers
  hosts: all
  gather_facts: true
  tasks:
    - name: install kafka broker
      ansible.builtin.import_role:
        name: infra.kafka.install
      vars:
        kafka_version: 3.8.0
        kafka_scala_version: 2.13
        kafka_role: broker
        kafka_data_dir: "/var/lib/kafka/data"
        kafka_cluster_id: "XeBwhcj6SfiR_07KLddO-w"
        kafka_broker_id_offset: 10
        kafka_broker_quorum_voters:
          - id: 1
            addr: controller
            port: 9093
```


## akhq
```yaml
- name: akhq
  hosts: all
  gather_facts: true
  tasks:
    - name: install akhq
      ansible.builtin.import_role:
        name: infra.kafka.akhq
      vars:
        akhq_version: 0.25.1
        akhq_bootstrap_servers:
          - name: molecule
            servers: broker:9092
```
