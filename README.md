# Ansible Role - PostgreSQL
[![Maintainer](https://img.shields.io/badge/maintained%20by-claranet-e00000?style=flat-square)](https://www.claranet.fr/)
[![License](https://img.shields.io/github/license/claranet/ansible-role-postgresql?style=flat-square)](LICENSE)
[![Release](https://img.shields.io/github/v/release/claranet/ansible-role-postgresql?style=flat-square)](https://github.com/claranet/ansible-role-postgresql/releases)
[![Status](https://img.shields.io/github/actions/workflow/status/claranet/ansible-role-postgresql/molecule.yml?branch=main&style=flat-square&label=tests)](https://github.com/claranet/ansible-role-postgresql/actions?query=workflow%3A%22Ansible+Molecule%22)
[![Ansible version](https://img.shields.io/badge/ansible-%3E%3D2.10-black.svg?style=flat-square&logo=ansible)](https://github.com/ansible/ansible)
[![Ansible Galaxy](https://img.shields.io/badge/ansible-galaxy-black.svg?style=flat-square&logo=ansible)](https://galaxy.ansible.com/claranet/postgresql)


> :star: Star us on GitHub — it motivates us a lot!

Install and configure PostgreSQL server on Debian and RedHat systems using this Ansible role. It provides a flexible and automated way to set up PostgreSQL databases, users, extensions, and more.

## Table of Contents

1. [Role Requirements](#warning-requirements)
2. [Role Dependencies](#arrows_counterclockwise-dependencies)
3. [Role Installation](#zap-role-installation)
4. [Features and Tags](#available-features-and-tags)
6. [Supported Linux/PostgreSQL Versions](#linuxpostgresql-versions-supported)
5. [Role features in use](#role-features-in-use)
    - [Proxy usage](#proxy-usage)
    - [Installation](#installation)
    - [Configuration](#configuration)
    - [Auto tuning](#auto-tuning)
    - [Physical replication](#physical-replication)
    - [Vacuum setup](#vacuum)
    - [Backup setup](#backup)
    - [User and database management](#createremove-database-users)
    - [Tablespaces management](#tablespaces)
    - [Databases management](#createremove-databases)
    - [Ownership and privileges management](#manage-ownership-and-privileges)
    - [Extensions management](#extensions-management)
    - [SQL executions](#sql-executions)
    - [Advanced customized installation](#advanced-customized-installation)
    - [Uninstallation](#uninstallation)
9. [Full example playbook](#pencil2-full-example-playbook)
10. [Hardening](HARDENING.md)
11. [Contributing](CONTRIBUTING.md)
12. [License](LICENSE)
13. [Author information](#author-information)

## :warning: Requirements

Ansible >= 2.10

## :arrows_counterclockwise: Collection dependencies
```yaml
- community.general
- community.postgresql==3.2.0
```


## :zap: Role Installation

```bash
ansible-galaxy install claranet.postgresql
```

### Available features and tags
-----
This role support the following features and tags in the following order during execution:
Feature                             | Tag
------------------------------------|---------------------
Uninstallation                      | uninstallation
Installation                        | install, installation
Datadir initialization              | init,initialize,initialise
Auto tune (with pg-config.org)      | autotune, auto-tune
Configuration                       | config, configure, configuration
Replication                         | repli, replication
Vacuum                              | vacuum
Backup                              | backup
User & membership management        | user, users
Tablespace management               | tblspc, tablespace, tablespaces
Database management                 | db, database, databases
Ownership & privileges management   | owner, owners, ownership, priv, privs, privileges
Extensions management               | ext, extension, extensions
SQL code executions                 | query, script


Linux/PostgreSQL versions supported
-----

Linux/PostgreSQL  |  12  |  13  |  14  |  15  | 16
------------------|:----:|:----:|:----:|:----:|:----:
Debian 11         | Yes  | Yes  | Yes  | Yes  |  Yes 
Debian 12         | Yes  | Yes  | Yes  | Yes  |  Yes 
Ubuntu 20.04      | Yes  | Yes  | Yes  | Yes  |  Yes 
Ubuntu 22.04      | Yes  | Yes  | Yes  | Yes  |  Yes 
Ubuntu 24.04      | Yes  | Yes  | Yes  | Yes  |  Yes 
RockyLinux 8.9    | Yes  | Yes  | Yes  | Yes  |  Yes 
RockyLinux 9.3    | Yes  | Yes  | Yes  | Yes  |  Yes 
Fedora 38         | No   | No   | No   | No   |  No  

## Role features in use

### Proxy usage
----
This role supports use of proxies.

The variables `postgresql_http_general_proxy` and `postgresql_https_general_proxy` can be used to specify a proxy for general internet access (such as downloading files).

The variables `postgresql_http_pkg_proxy` and `postgresql_https_pkg_proxy` can be used to specify a proxy for package manager interaction (such as downloading packages or updating cache).

_Notes:_ 

These variables are translated to environnement variables `http_proxy` and `https_proxy` which are passed to corresponding tasks.


### Installation
----
_default PostgreSQL version is 15_
PostgreSQL and locales installation.

```yaml
postgresql_version: "15"

# Debian only. Used to generate the locales used by PostgreSQL databases.
postgresql_locales:
  - 'en_US.UTF-8'
  - 'fr_FR.UTF-8'

# Redhat only. For more info check: https://www.thegeekdiary.com/how-to-add-locale-on-centos-rhel-8/
postgresql_locale_packages:
  - glibc-langpack-en
  - glibc-langpack-fr
```

### Configuration 
----
Example for configuration related variables:
```yaml
postgresql_port: 5432
postgresql_listen_addresses: 0.0.0.0
postgresql_shared_preload_libraries:
  - pg_stat_statements
postgresql_max_connections: 100
# Custom PostgreSQL configuration options provided by the user
postgresql_global_config_options_extra:
  - option: log_statement
    value: all
postgresql_hba_entries_extra: []
  # - {contype: local, databases: all, users: postgres, method: peer}
# Default authentication method used method for the default hba rules
# postgresql_auth_method: "{{ ansible_fips | ternary('scram-sha-256', 'md5') }}"
postgresql_hba_use_raw: false
postgresql_hba_raw: |
  # TYPE  DATABASE        USER        ADDRESS         METHOD
  local   all             postgres                    peer
  host    all             all         127.0.0.1/32    md5
  host    all             all         ::1/128         md5

# Allow service restart for configuration changes that require it
postgresql_config_change_allow_restart: true

```

_Notes:_

By default, this role restarts the PostgreSQL service during subsequent configuration changes after the initial engine installation, ensuring all changes are applied immediately. However, this behavior can cause potential service outages.

To prevent automatic restarts, you can set the variable `postgresql_config_change_allow_restart` (introduced in `v2.1.0`) to `false`. Starting with (`v3.0.0`), the default value of this variable will change to `false`, meaning the role will avoid restarting PostgreSQL by default. If you rely on the current behavior, you will need to explicitly set this variable to true in your configuration.

In relation to HBA rules, you have the option to configure the variable `postgresql_hba_use_raw` as `true` and specify the contents of `postgresql_hba_raw`. These contents will be inserted directly into the `pg_hba.conf` file.

Alternatively, if you possess a file containing these rules, you can set the `postgresql_hba_template_path` variable to the path of that file on the Ansible controller. In this case, the specified file will be copied to replace the `pg_hba.conf` file.

However, it's crucial to note that when using this approach, the entire content of the HBA file becomes your responsibility. You must ensure that there are rules allowing the `postgres` system user to connect to the PostgreSQL server without requiring a password and authorizing replication in the relevant context


### Auto tuning
----
This role supports the use of the website [pgconfig.org](https://www.pgconfig.org) for automatically tunning some of configuration parameters of the postgresql server.

You can check the [full documentation](https://docs.pgconfig.org/api/#available-parameters) on the available configurations parameters.

Configuration example for variables (_those are the default values_):
```yaml
postgresql_autotune: true
postgresql_autotune_base_url: https://api.pgconfig.org
postgresql_autotune_pg_version: "{{ postgresql_version }}"
# linux/windows/unix
postgresql_autotune_os_type: linux
# 386/x86-64
postgresql_autotune_arch: x86-64
# HDD/SSD/SAN
postgresql_autotune_drive_type: SSD
# WEB/OLTP/DW/Mixed/Desktop
postgresql_autotune_env_name: OLTP
postgresql_autotune_cpus: "{{ ansible_processor_nproc | d('') }}"
# Total ram in GB
postgresql_autotune_total_ram: "{{ ((ansible_memtotal_mb / 1024) | round | int) | d('') }}"
```


### Physical Replication
----
Configuration example for the primary server: 

```yaml
postgresql_replication: true
postgresql_replication_user: replication_user
postgresql_replication_password: replication_password

postgresql_replication_role: primary
# Used to generate hba rules to allow the specified servers to connect to the primary server
postgresql_replication_replica_addresses: [192.168.1.6/32, 192.168.1.7/32]
# User provided replication specific hba rules that overwrites the generated ones
postgresql_replication_hba_entries: []
  # - contype: host
  #   databases: replication
  #   users: "{{ postgresql_replication_user }}"
  #   address: "{{ postgresql_replication_replica_address }}"
  #   method: "{{ postgresql_replication_auth_method }}"

```


Configuration example for the replicas:

```yaml
postgresql_replication: true
postgresql_replication_user: replication_user
postgresql_replication_password: replication_password

postgresql_replication_role: replica
postgresql_replication_primary_address: 192.168.1.5
postgresql_replication_primary_port: 5432
postgresql_replication_primary_inventory_name: node1 # primary server name in the ansible inventory

```

Using slots for replication:

```yaml
postgresql_replication_slot: replica1_slot
postgresql_replication_create_slot: true
```
When set to true the variable `postgresql_replication_create_slot` ensures the specified replication slot exists before running the `pg_basebackup` command run to copy data from the primary.

_Notes:_  

When using the slot feature for replication, make sure to indicate a different slot for each replica. You can set that value in the host_vars for each server.


Advanced configuration:
```yaml
# Authentication method specific for the replica hosts
# postgresql_replication_auth_method: "{{ postgresql_auth_method }}"
# --checkpoint parameter value of the pg_basebackup command
postgresql_pg_basebackup_checkpoint: fast   # spread
# --wal-method parameter value of the pg_basebackup command
postgresql_pg_basebackup_walmethod: stream  # none/stream/fetch
# extra arguments appended to the build pg_basebackup command
postgresql_pg_basebackup_args: ""

# Actual pg_basebackup built with the previous parameters
# DO NOT override this variable except you know what you are doing 
postgresql_pg_basebackup_cmd: {{ _postgresql_bin_path }}/pg_basebackup --no-password --host {{ postgresql_replication_primary_address }} --port {{ postgresql_replication_primary_port }} --username {{ postgresql_replication_user }} --pgdata {{ _postgresql_data_dir }} --checkpoint {{ postgresql_pg_basebackup_checkpoint }} {{ (postgresql_replication_slot != '') | ternary('--slot ' ~ postgresql_replication_slot, '') }} --wal-method {{ postgresql_pg_basebackup_walmethod }} --write-recovery-conf --verbose --progress {{ postgresql_pg_basebackup_args }}
```

### Vacuum
----
_(new in v2.0.0)_

By default vaccum is enabled (`postgresql_vacuum: true`), with vacuum and analyze planned daily at 23:00

Configuration example for vacuum.

To disable:
```yaml
postgresql_vacuum: false
```

To change schedule to 21:00: 
```yaml
postgresql_vacuum_schedule:
  minute: 0
  hour: 21
```

To vacuum only (other options : vacuumanalyze, vacuumfull, vacuumonly, analyzeonly)
```yaml
postgresql_vacuum_option: "vacuumonly"
```

### Backup
----
> :rotating_light: The provided backup script is not intended for use within Claranet environments. Claranet has superior and more robust backup solutions that should be used for production systems. This script is designed solely for development, testing, or demonstration purposes and should not replace established backup practices in live environments. :rotating_light:

By default, the backup is disabled (`postgresql_backup: false`).

Configuration example for backup.
```yaml
# Allow ansible to setup postgresql backups when running
postgresql_backup: true
# Root directory containing the backups
postgresql_backup_root_dir: /var/backups/postgresql
postgresql_backup_mail_addr: admin@email.com
postgresql_backup_schedule:
    hour: 0
    minute: 0
# 3 days retentions for daily backups
postgresql_backup_brdaily: 3
# disable weekly and monthly backups
postgresql_backup_doweekly: 0
postgresql_backup_domonthly: 0
# Weekly and monthly backups are disabled so these values don't really matter
postgresql_backup_brweekly: 0
postgresql_backup_brmontly: 0
```

### Create/Remove database users
----
Configuration example for managing users:

```yaml
postgresql_users:
# Create two groups 'group1' and 'group2' by making use of thr role_attr_flags attribute
  - name: group1
    role_attr_flags: NOLOGIN
  - name: group2
    role_attr_flags: NOLOGIN
# Create 'user1' and 'user2' with default parameters
  - name: user1
  - name: user2
# Create user 'jdoe' with more personalized parameters
  - name: jdoe
    password: password
    comment: this is a test user
    expires: "Jun 21 2029"

postgresql_memberships:
# Ensure the role 'user1' belongs to group 'group1'
  - groups:
    - group1
    target_roles:
    - user1
    state: present
# Ensure the role 'user2' does not belong to the group 'group2'
  - groups:
    - group2
    target_roles:
    - user2
    state: absent
# Ensure the role 'jdoe' does not belong to any group
  - groups: []
    target_roles:
    - jdoe
    state: exact
```

_Notes:_

Check the links for a documentation on all the available options for defining items within the variables:
- [`postgresql_users`](https://docs.ansible.com/ansible/latest/collections/community/postgresql/postgresql_user_module.html#parameters)
- [`postgresql_memberships`](https://docs.ansible.com/ansible/latest/collections/community/postgresql/postgresql_membership_module.html#parameters).


### Tablespaces
----

COnfiguration example for managing tablespaces:

```yaml
postgresql_tablespaces:
# Create tablespace 'ssd'
  - name: ssd
    set:
      random_page_cost: 1
      seq_page_cost: 1
    owner: jdoe
    location: /tmp/ssd
    location_create: true # default is false
    state: present # default is present
    location_owner: postgres # default is postgres
    location_group: postgres # default is postgres
    location_mode: '0700' # default is '0700'
# Delete tablespaces 'temp2'
  - name: temp2
    state: absent
    location: /tmp/temp2_tblspc
    set:
      random_page_cost: 1
    owner: user1
```

_Notes:_

When combining `location_create: true` with `state: present` the role will create the location of the tablespace with the specified permissions before creating the tablespace itself.

If you ensure the existence of that location by others means, feel free to not set the variables `location_*`.


### Create/Remove databases
----

Configuration example for managing databases:

```yaml
postgresql_databases:
  - name: db1
    owner: user1
    encoding: UTF-8
    lc_collate: en_US.UTF-8
    lc_ctype: en_US.UTF-8
    conn_limit: 100
    template: template0
  - name: db2
    owner: user2
  - name: db3
    state: absent

postgresql_schemas:
  - name: acme
    db: db1
  - name: acme
    db: db2
  - name: not_existing_shema
    db: db1
    owner: user1
    state: absent
    cascade_drop: true

postgresql_tables:
  - name: table1
    db: db1
    owner: user1
    columns:
      - id SERIAL PRIMARY KEY
      - name VARCHAR(50)
      - age INT
      - email VARCHAR(100)
    tablespace: ssd
    storage_params:
      - fillfactor=10
      - autovacuum_analyze_threshold=1
  - name: acme.table2
    db: db1
    columns: waste_id int
    unlogged: true
```

_Notes:_

Check the links for a documentation on all the available options for defining items within the variables:
- [`postgresql_database`](https://docs.ansible.com/ansible/latest/collections/community/postgresql/postgresql_database_module.html#parameters)
- [`postgresql_schema`](https://docs.ansible.com/ansible/latest/collections/community/postgresql/postgresql_schema_module.html#parameters)
- [`postgresql_table`](https://docs.ansible.com/ansible/latest/collections/community/postgresql/postgresql_table_module.html#parameters)

### Manage ownership and privileges
----
```yaml
postgresql_privs:
  - roles: group1 # group1 and user1 are granted all privs on all object wihtin the public schema of the example db
    db: db1
    privs: ALL
    objs: table1
    type: table
    # schema: public
    grant_option: true
  - roles: user2 # grant user2 user all privs on postgres database
    db: postgres
    type: database
    privs: ALL
    objs: db1,db2
    grant_option: true
  - roles  : group1 # grant group1 role all privs on all tables and all sequences of database db1
    db: db1
    objs: TABLES,SEQUENCES
    privs: ALL
    type: default_privs


postgresql_ownerships:
  - db: db1
    new_owner: user1
    obj_name: table1
    obj_type: table
  - db: db2 # reassign all dbs owned by user1 to user2 and all objects in db2 to user2
    new_owner: user2
    reassign_owned_by: user1
```
_Notes:_

Check the links for a documentation on all the available options for defining items within the variables:
- [`postgresql_ownerships`](https://docs.ansible.com/ansible/latest/collections/community/postgresql/postgresql_owner_module.html#parameters) 
- [`postgresql_privs`](https://docs.ansible.com/ansible/latest/collections/community/postgresql/postgresql_privs_module.html#parameters)



### Extensions management
----
Configuration example for extensions management:

```yaml
postgresql_extensions:
  - name: pg_stat_statements
    db: db1
    cascade: true
    version: latest
    schema: public
  - name: non_existing_extension
    db: db1
    state: absent
```

_Notes:_

For the extensions with `state: present, version: latest`, the role will always report `changed: false` as the underlying module does not differentiate when the extension is actually updated or not.



### SQL executions
----
Configuration example for running sql:
```yaml
postgresql_queries:
  - query: SELECT version()
    db: db1
  - query:
      - select * from public.table1
    db: db1
postgresql_scripts:
  - path: /tmp/insert_in_table1.sql
    db: db1
```

_Notes:_

Check the links for a documentation on all the available options for defining items within the variables:
- [`postgresql_queries`](https://docs.ansible.com/ansible/latest/collections/community/postgresql/postgresql_query_module.html#parameters)
- [`postgresql_scripts`](https://docs.ansible.com/ansible/latest/collections/community/postgresql/postgresql_script_module.html#parameters).


### Advanced customized installation
----
It is highly recommended you modify these variables only if you know what you're doing.
```yaml
# New postgresql installation datadir
postgresql_data_dir: 
# Extra arguments passed to the initdb binary during database initialization
postgresql_initdb_extra_args: ''
# Debian only. postgresql cluster name
postgresql_cluster_name: main

# PostgreSQL system user/group
postgresql_user: postgres
postgresql_group: postgres

# Postgresql service state after role run
postgresql_service_state: started
# Whether or not to enable the postgresql service after installation
postgresql_service_enabled: true
# PostgreSQL unix_socket_directories config parameter
postgresql_unix_socket_directories: [/run/postgresql]

# Permissions for the PostgreSQL unix sockets (default is distro dependant)
postgresql_unix_socket_directories_mode: ''

# Permissions for the postgresql log directory
postgresql_log_directory_mode: '0700'
# Whether or not to create a tmpfiles.d postgresql file to persist permissions on unix socket directories and log directories accross system rebbots 
postgresql_persist_permissions: true
# Path to the template used by Ansible to create the tempfile conf to persist permissions 
# You can update this path to a custom file to completely customize the persisting rules
postgresql_tempfile_src_template_path: etc/tmpfiles.d/postgresql-common.conf.j2
# Destination path for the tempfile configuration
postgresql_tempfile_dest_path: /etc/tmpfiles.d/postgresql-common.conf
# File permissions and owner/group of the postgresql tempfile configuration
postgresql_tempfile_mode: '0644'
postgresql_tempfile_owner: root
postgresql_tempfile_group: root

```

### Uninstallation
----
If you want to uninstall a Postgresql installation with this role, set both variables `postgresql_uninstall_1`, `postgresql_uninstall_1` to `true` and use the corresponding tag (`uninstallation`).

## :pencil2: Full Example Playbook

```yaml
---
- name: Converge
  hosts: all
  become: true
  gather_facts: true

  vars:
    postgresql_version: "15"

    # Run debug tasks withint the role 
    postgresql_debug: true

    # Configuration
    postgresql_port: 5432
    postgresql_listen_addresses: 0.0.0.0
    postgresql_shared_preload_libraries:
      - pg_stat_statements
    postgresql_max_connections: 100
    # Custom configuration options provided by the user
    postgresql_global_config_options_extra:
      - option: log_statement
        value: all
    postgresql_hba_entries_extra: []
      # - {contype: local, databases: all, users: postgres, method: peer}

    postgresql_autotune: true
    # postgresql_autotune_base_url: http://192.168.56.101:3000

    postgresql_users_no_log: false
    postgresql_users:
    # Create two groups 'group1' and 'group2' by making use of thr role_attr_flags attribute
      - name: group1
        role_attr_flags: NOLOGIN
      - name: group2
        role_attr_flags: NOLOGIN
    # Create 'user1' and 'user2' with default parameters
      - name: user1
      - name: user2
    # Create user 'jdoe' with more personalized parameters
      - name: jdoe
        password: password
        comment: this is a test user
        expires: "Jun 21 2029"

    postgresql_memberships:
    # Ensure the role 'user1' belongs to group 'group1'
      - groups:
        - group1
        target_roles:
        - user1
        state: present
    # Ensure the role 'user2' does not belong to the group 'group2'
      - groups:
        - group2
        target_roles:
        - user2
        state: absent
    # Ensure the role 'jdoe' does not belong to any group
      - groups: []
        target_roles:
        - jdoe
        state: exact

    postgresql_tablespaces:
    # Create tablespace 'ssd'
      - name: ssd
        set:
          random_page_cost: 1
          seq_page_cost: 1
        owner: jdoe
        location: /tmp/ssd
        location_create: true # default is false
        state: present # default is present
        location_owner: postgres # default is postgres
        location_group: postgres # default is postgres
        location_mode: '0700' # default is '0700'
    # Delete tablespaces 'temp2'
      - name: temp2
        state: absent
        location: /tmp/temp2_tblspc
        set:
          random_page_cost: 1
        owner: user1

    postgresql_databases:
      - name: db1
        owner: user1
        encoding: UTF-8
        lc_collate: en_US.UTF-8
        lc_ctype: en_US.UTF-8
        conn_limit: 100
        template: template0
      - name: db2
        owner: user2
      - name: db3
        state: absent

    postgresql_schemas:
      - name: acme
        db: db1
      - name: acme
        db: db2
      - name: not_existing_shema
        db: db1
        state: absent
        cascade_drop: true

    postgresql_tables:
      - name: table1
        db: db1
        owner: user1
        columns:
          - id SERIAL PRIMARY KEY
          - name VARCHAR(50)
          - age INT
          - email VARCHAR(100)
        tablespace: ssd
        storage_params:
          - fillfactor=10
          - autovacuum_analyze_threshold=1
      - name: acme.table2
        db: db1
        columns: waste_id int
        unlogged: true
      #   like: public.table1
      #   including: comments, indexes
      # - name: table2
      #   db: db1
      #   truncate: true
      # - name: acme.table2
      #   db: db1
      #   like: public.table2
      # - name: table2
      #   db: db2
      #   state: absent
      #   cascade: true


    postgresql_extensions:
      - name: pg_stat_statements
        db: db1
        cascade: true
        version: latest
        schema: public
      - name: non_existing_extension
        db: db1
        state: absent


    postgresql_queries:
      - query: SELECT version()
        db: db1
      - query:
          - select * from public.table1
        db: db1
    postgresql_scripts:
      - path: /tmp/insert_in_table1.sql
        db: db1

    postgresql_privs:
      - roles: group1 # group1 and user1 are granted all privs on all object wihtin the public schema of the example db
        db: db1
        privs: ALL
        objs: table1
        type: table
        # schema: public
        grant_option: true
      - roles: user2 # grant nreslou user all privs on nreslou database by first connecting to the postgres maintenance db
        db: postgres
        type: database
        privs: ALL
        objs: db1,db2
        grant_option: true
      # - roles: user1
      #   db: db2
      #   type: function
      #   objs: add(int:int)
      #   privs: ALL
      #   grant_option: true

    postgresql_ownerships:
      - db: db1
        new_owner: user1
        obj_name: table1
        obj_type: table
      # - db: db2 # reassign all dbs owned by user1 to user2 and all objects in db2 to user2
      #   new_owner: user2
      #   reassign_owned_by: user1

    # standalone installation
    postgresql_replication: false

    # Disable backups setup by Ansible
    postgresql_backup: false


  roles:
    - role: claranet.postgresql
```

## :closed_lock_with_key: [Hardening](HARDENING.md)

## :heart_eyes_cat: [Contributing](CONTRIBUTING.md)
Checkout the [Contributing](CONTRIBUTING.md) if you are looking for a guide on how to setup an environnement so you can test this role as a developper.


## :copyright: [License](LICENSE)

[Mozilla Public License Version 2.0](https://www.mozilla.org/en-US/MPL/2.0/)

## Author information

Proudly made by the Claranet team and inspired by:
- [Jeff Geerling](https://github.com/geerlingguy/ansible-role-postgresql)
