# jenkins

Ansible collection that installs jenkins.

# Compatibility
The collection was tested on the following platforms:
- Debian 12 (x86 & aarch64)
- AlmaLinux 9 (x86 & aarch64)
- Amazon Linux 2023 (x86 & aarch64)

# Usage

```yaml
- name: example
  hosts: all
  gather_facts: true
  tasks:
    - name: install jenkins
      ansible.builtin.import_role:
        name: infra.jenkins.install
      vars:
        jenkins_version: 2.462.2
        jenkins_home: /var/lib/jenkins
        jenkins_working_dir: /var/lib/jenkins
        jenkins_show_initial_admin_password: true
```
