from _base import AciAction
import json


class ContractCreate(AciAction):
    def run(self, cluster_name, tenant_name, name):
        from cobra.internal.codec.jsoncodec import toJSONStr

        import cobra.mit.naming
        import cobra.mit.request
        import cobra.model.vz

        # connect to apic
        md = self._login(cluster_name)

        # the top level object on which operations will be made
        topParentDn = cobra.mit.naming.Dn.fromString('uni/tn-' + tenant_name)
        topMo = md.lookupByDn(topParentDn)

        # build the request using cobra syntax
        vzBrCP = cobra.model.vz.BrCP(topMo, ownerKey='', name=name, descr='', targetDscp='unspecified', nameAlias='', ownerTag='', prio='unspecified')

        # commit the generated code to APIC
        c = cobra.mit.request.ConfigRequest()
        c.addMo(topMo)
        md.commit(c)

        return json.loads(toJSONStr(topMo))
