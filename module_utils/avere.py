#!/usr/bin/env python

import vFXT


def avere_host_argument_spec():
    return dict(
        hostname=dict(type='str', required=True),
        username=dict(type='str', required=True),
        password=dict(type='str', required=True, no_log=True),
    )


def avere_api_client(module):
    hostname = module.params.get('hostname')
    username = module.params.get('username')
    password = module.params.get('password')

    client = vFXT.xmlrpcClt.getXmlrpcClient(
        "http://{0}/cgi-bin/rpc2.py".format(hostname),
        do_cert_checks=False
    )

    login = client.system.login(
        username.encode('base64'),
        password.encode('base64')
    )
    if login != 'success':
        raise Exception(result)

    return client
