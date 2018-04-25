from _base import AciAction
import json


class ContractAttach(AciAction):
    def run(self, cluster_name, tenant_name, contract_name, parent_name, name, type_of_endpoint, type_of_consumption):
        from cobra.internal.codec.jsoncodec import toJSONStr

        import cobra.mit.naming
        import cobra.mit.request
        import cobra.model.fv

        # connect to apic
        md = self._login(cluster_name)

        if type_of_endpoint == "EPG":
            # the top level object on which operations will be made
            topParentDn = cobra.mit.naming.Dn.fromString("uni/tn-{tenant_name}/ap-{parent_name}/epg-{name}".format(
                tenant_name=tenant_name,
                parent_name=parent_name,
                name=name
                ))
            topMo = md.lookupByDn(topParentDn)

        elif type_of_endpoint == "EN":
            # the top level object on which operations will be made
            topParentDn = cobra.mit.naming.Dn.fromString("uni/tn-{tenant_name}/out-{parent_name}/instP-{name}".format(
                tenant_name=tenant_name,
                parent_name=parent_name,
                name=name
                ))
            topMo = md.lookupByDn(topParentDn)

        else:
            return (False, {
                                "error": "bad endpoint Type",
                                "type_of_endpoint": type_of_endpoint
                            })

        # build the request using cobra syntax
        if type_of_consumption == "Consumer":
            fvRsCons = cobra.model.fv.RsCons(topMo, tnVzBrCPName=contract_name, prio='unspecified')

        elif type_of_consumption == "ConsumerImport":
            fvRsConsIf = cobra.model.fv.RsConsIf(topMo, tnVzCPIfName=contract_name, prio='unspecified')

        elif type_of_consumption == "Provider":
            fvRsProv = cobra.model.fv.RsProv(topMo, tnVzBrCPName=contract_name, matchT='AtleastOne', prio='unspecified')

        else:
            return (False, {
                                "error": "bad consumption type",
                                "type_of_consumption": type_of_consumption
                            })



        # commit the generated code to APIC
        c = cobra.mit.request.ConfigRequest()
        c.addMo(topMo)
        md.commit(c)

        return json.loads(toJSONStr(topMo))
