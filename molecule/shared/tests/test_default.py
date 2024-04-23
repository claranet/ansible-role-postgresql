#!/usr/bin/env python

import os
import stat
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")

# def test_shell(host):
#     command = host.run("sh --version")
#     assert command.rc == 0

# def test_service(host):
#     service = host.service("postgresql")
#     assert service.is_enabled
#     assert service.is_running

def test_listen_port(host):
    #host.socket.get_listening_sockets()
    assert host.socket("tcp://0.0.0.0:5432").is_listening