#!/usr/bin/python

# Copyright: (c) 2023, Sean Nelson <hyperkineticnerd@gmail.com>
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: cosign_login

short_description: Use cosign to login to a registry

version_added: "1.0.0"

description: This is my longer description explaining my test module.

options:
    registry:
        description: Registry to login to using cosign
        required: true
        type: str
    username:
        description: Username to use for login
        required: true
        type: str
    password:
        description: Password for login
        required: true
        type: str

author:
    - Sean Nelson (@hyperkineticnerd)
'''

EXAMPLES = r'''
- name: Login using Username and Password
  hyperkineticnerd.sigstore.cosign_login:
    registry: registry.example.com
    username: alice
    password: changeme
'''

RETURN = r'''
rc:
    description: The return-code from cosign.
    type: int
    returned: always
    sample: '0'
stdout:
    description: The stdout from cosign.
    type: str
    returned: always
    sample: ''
stderr:
    description: The stderr from cosign.
    type: str
    returned: always
    sample: ''
'''

from ansible.module_utils.basic import AnsibleModule
import subprocess


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        registry=dict(type='str', required=True),
        username=dict(type='str', required=True),
        password=dict(type='str', required=True, no_log=True)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        cmd='',
        rc=1,
        stdout='',
        stderr=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    subproc_cmd = [
        "cosign", "login",
        module.params['registry'],
        "-u", module.params['username'],
        "-p", module.params['password']
    ]

    if module.check_mode:
        result.update({
            'cmd': subproc_cmd.join(' ')
        })
        module.exit_json(**result)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    subproc_ret = subprocess.run(subproc_cmd)

    result.update({
        'rc': subproc_ret.returncode,
        'stderr': subproc_ret.stderr,
        'stdout': subproc_ret.stdout
    })

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    if result['rc'] == 0:
        result['changed'] = True

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
