#!/bin/bash
#
# Script to quickly deploy apps without
# requiring all credentials for provisioning.
# Deploys apps in `./deploy` directory (symlink to ansible template dir).
# Make sure to have team19.pem loaded
# e.g. `ssh-agent $SHELL && ssh-add team19.pem`.

cd devops/platform/chirp/ansible/
export ANSIBLE_HOST_KEY_CHECKING=False
ansible-playbook -i hosts site.yml
