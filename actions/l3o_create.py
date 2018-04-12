from _base import AciAction
import json


class L3oCreate(AciAction):
    def run(self, cluster_name, tenant_name,
                name,
                vrf_name=None,
                l3_external_domain_name=None
            ):
        from cobra.internal.codec.jsoncodec import toJSONStr

        import cobra.mit.naming
        import cobra.mit.request
        import cobra.model.l3ext

        # connect to apic
        md = self._login(cluster_name)

        # the top level object on which operations will be made
        topParentDn = cobra.mit.naming.Dn.fromString('uni/tn-' + tenant_name)
        topMo = md.lookupByDn(topParentDn)

        # build the request using cobra syntax
        l3extOut = cobra.model.l3ext.Out(topMo, ownerKey='', name=name, descr='', targetDscp='unspecified', enforceRtctrl='export', nameAlias='', ownerTag='')

        if vrf_name is not None:
            l3extRsEctx = cobra.model.l3ext.RsEctx(l3extOut, tnFvCtxName=vrf_name)

        if l3_external_domain_name is not None:
            l3extRsL3DomAtt = cobra.model.l3ext.RsL3DomAtt(l3extOut, tDn='uni/l3dom-' + l3_external_domain_name)

        # commit the generated code to APIC
        c = cobra.mit.request.ConfigRequest()
        c.addMo(topMo)
        md.commit(c)

        return json.loads(toJSONStr(topMo))
