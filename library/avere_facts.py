#!/usr/bin/env python

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.avere \
    import avere_api_client, avere_host_argument_spec


def main():
    module = AnsibleModule(
        argument_spec=avere_host_argument_spec(),
        supports_check_mode=True,
    )

    result = {'changed': False}

    client = avere_api_client(module)

    result['cache_policies'] = client.cachePolicy.list()

    result['cloud_credentials'] = client.corefiler.listCredentials()

    result['cluster'] = client.cluster.get()

    corefilers = client.corefiler.list()
    result['corefilers'] = {}
    for corefiler in corefilers:
        corefiler_facts = client.corefiler.get(corefiler)
        corefiler_facts[corefiler]['nfs_exports'] = \
            client.corefiler.listExports(corefiler)
        result['corefilers'].update(corefiler_facts)

    result['migrations'] = client.migration.list()

    result['schedules'] = client.cluster.listSchedules()

    result['snapshot_policies'] = client.snapshot.listPolicies()

    vservers = client.vserver.list()
    result['vservers'] = {}
    for vserver in vservers:
        vserver_facts = client.vserver.get(vserver)
        vserver_facts[vserver]['cifs_shares'] = \
            client.cifs.listShares(vserver)
        vserver_facts[vserver]['junctions'] = \
            client.vserver.listJunctions(vserver)
        vserver_facts[vserver]['nfs_exports'] = {}
        for corefiler in corefilers:
            vserver_facts[vserver]['nfs_exports'][corefiler] = \
                client.nfs.listExports(vserver, corefiler)
        nfs_export_policies = client.nfs.listPolicies(vserver)
        vserver_facts[vserver]['nfs_export_policies'] = {}
        for nfs_export_policy in nfs_export_policies:
            (vserver_facts[vserver]
                ['nfs_export_policies'][nfs_export_policy]) = \
                client.nfs.listRules(vserver, nfs_export_policy)
        result['vservers'].update(vserver_facts)

    module.exit_json(**result)


if __name__ == '__main__':
    main()
