# Platform Launch

Platform Launch provisions and configures a cluster from scratch for use of
twitter analysis on OpenStack.

## Requirements

Software:
- Bash 4.3+
- Ansible 1.9+
- Terraform 0.5+
- j2cli 0.3+

## Usage

Prerequisites:
- Ensure the SSH keypair assigned to the cluster is available via ssh-agent.
  This is required for Ansible.
- Expose OpenStack credentials as environment variables.
- Expose DNSimple credentials as environment variables.

To configure:
- Adjust `./platform-config.sh` to the platform to be built.
- Adjust `$PLATFORM/cluster-config.sh` where `$PLATFORM` is the desired platform
  found in `./platform-config.sh`.

To launch or update existing build (idempotent):
- Run `./build-cluster.sh`.

To remove:
- Run `./destroy-cluster.sh`.
