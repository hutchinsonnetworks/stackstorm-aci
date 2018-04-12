from _base import AciAction
import json


class L3oInterfaceProfileCreate(AciAction):
    def run(self, cluster_name, tenant_name, l3o_name, node_profile_name, name):
        from cobra.internal.codec.jsoncodec import toJSONStr

        import cobra.mit.naming
        import cobra.mit.request
        import cobra.model.l3ext

        # connect to apic
        md = self._login(cluster_name)

        # the top level object on which operations will be made
        topDn = cobra.mit.naming.Dn.fromString('uni/tn-' + tenant_name + '/out-' + l3o_name + "/lnodep-" + node_profile_name + "/lifp-" + name)
        topParentDn = topDn.getParent()
        topMo = md.lookupByDn(topParentDn)

        # build the request using cobra syntax
        l3extLIfP = cobra.model.l3ext.LIfP(topMo, ownerKey='', name=name, descr='', tag='yellow-green', nameAlias='', ownerTag='')
        l3extRsEgressQosDppPol = cobra.model.l3ext.RsEgressQosDppPol(l3extLIfP, tnQosDppPolName='')
        l3extRsIngressQosDppPol = cobra.model.l3ext.RsIngressQosDppPol(l3extLIfP, tnQosDppPolName='')
        l3extRsNdIfPol = cobra.model.l3ext.RsNdIfPol(l3extLIfP, tnNdIfPolName='')

        # commit the generated code to APIC
        c = cobra.mit.request.ConfigRequest()
        c.addMo(topMo)
        md.commit(c)

        return json.loads(toJSONStr(topMo))
