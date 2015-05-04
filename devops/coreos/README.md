# CoreOS Launch

CoreOS Launch provisions and configures a cluster from scratch for use of
twitter analysis on OpenStack.

## Requirements

Software:
- Standard linux tools
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
- Adjust `./cluster-config.sh`

To launch or update existing build (idempotent):
- Run `./build-cluster.sh`.

To remove:
- Run `./destroy-cluster.sh`.
