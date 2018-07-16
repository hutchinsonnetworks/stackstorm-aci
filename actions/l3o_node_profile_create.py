from _base import AciAction
import json


class L3oNodeProfileCreate(AciAction):
    def run(self, cluster_name, tenant_name, l3o_name,name):
        from cobra.internal.codec.jsoncodec import toJSONStr

        import cobra.mit.naming
        import cobra.mit.request
        import cobra.model.l3ext

        # connect to apic
        md = self._login(cluster_name)

        # the top level object on which operations will be made
        topParentDn = cobra.mit.naming.Dn.fromString('uni/tn-' + tenant_name + '/out-' + l3o_name)
        topMo = md.lookupByDn(topParentDn)

        # build the request using cobra syntax
        l3extLNodeP = cobra.model.l3ext.LNodeP(topMo, ownerKey='', name=name, descr='', targetDscp='unspecified', tag='yellow-green', nameAlias='', ownerTag='')

        # commit the generated code to APIC
        c = cobra.mit.request.ConfigRequest()
        c.addMo(topMo)
        md.commit(c)

        return json.loads(toJSONStr(topMo))
