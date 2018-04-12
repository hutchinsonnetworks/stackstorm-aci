from _base import AciAction
import json

class TenantCreate(AciAction):
    def run(self, cluster_name, name, description=''):
        from cobra.internal.codec.jsoncodec import toJSONStr

        import cobra.mit.naming
        import cobra.mit.request
        import cobra.model.fv

        # connect to apic
        md = self._login(cluster_name)

        # the top level object on which operations will be made
        topDn = cobra.mit.naming.Dn.fromString('uni/tn-' + name)
        topParentDn = topDn.getParent()
        topMo = md.lookupByDn(topParentDn)

        # build the request using cobra syntax
        fvTenant = cobra.model.fv.Tenant(topMo, ownerKey='', name=name, descr=description, nameAlias='', ownerTag='')

        # commit the generated code to APIC
        c = cobra.mit.request.ConfigRequest()
        c.addMo(fvTenant)
        md.commit(c)

        return json.loads(toJSONStr(topMo))
