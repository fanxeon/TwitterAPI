#!/usr/bin/env python
#
# Produces ansible hostfile from Terraform.
# Arguments: terraform-statefile
# 
# Requires terraform output:
# ips - newline delimited list of ip addresses of nodes.
# 

from __future__ import print_function
import json
import os
import sys

def get_terraform_outputs(statefile):
    with open(statefile) as handle:
        state = json.load(handle)
        modules = state['modules']
        root = filter(lambda x: x['path'] == ['root'], modules)[0]
        outputs = root['outputs']
        return outputs

def main():
    # Argument check
    if len(sys.argv) != 2:
        print(
            'usage: {0} terraform-state-file'.format(sys.argv[0]),
            file=sys.stderr
        )
        sys.exit(1)

    # Get IP addresses of machines
    outputs = get_terraform_outputs(sys.argv[1])
    ips = outputs['ips'].split('\n')

    # Get required env variables
    peer_name_prefix = os.environ['PEER_NAME_PREFIX']
    subdomain = os.environ['SUBDOMAIN']
    domain = os.environ['DOMAIN']

    # Export each node with ID
    print('[chirp]')
    node_id = 1
    for ip in ips:
        hostname = '{0}{1}.{2}.{3}'.format(
            peer_name_prefix,
            node_id,
            subdomain,
            domain
        )
        templ = '{0} ansible_ssh_host={1} node_id={2} node_name={3}{2}'
        node_line = templ.format(
            hostname,
            ip,
            node_id,
            peer_name_prefix
        )
        print(node_line)

        node_id += 1


if __name__ == '__main__':
    main()
