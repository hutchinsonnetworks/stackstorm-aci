from _base import AciAction
import json


class L3oNodeCreate(AciAction):
    def run(self, cluster_name, tenant_name, l3o_name, node_profile_name, node_id, router_id):
        from cobra.internal.codec.jsoncodec import toJSONStr

        import cobra.mit.naming
        import cobra.mit.request
        import cobra.model.l3ext

        # connect to apic
        md = self._login(cluster_name)

        # the top level object on which operations will be made
        topParentDn = cobra.mit.naming.Dn.fromString('uni/tn-' + tenant_name + '/out-' + l3o_name + "/lnodep-" + node_profile_name)
        topMo = md.lookupByDn(topParentDn)

        l3extRsNodeL3OutAtt = cobra.model.l3ext.RsNodeL3OutAtt(topMo, rtrIdLoopBack='yes', rtrId=router_id, tDn='topology/pod-1/node-' + node_id)
        l3extInfraNodeP = cobra.model.l3ext.InfraNodeP(l3extRsNodeL3OutAtt, nameAlias='', fabricExtCtrlPeering='no', descr='', name='')


        # commit the generated code to APIC
        c = cobra.mit.request.ConfigRequest()
        c.addMo(topMo)
        md.commit(c)

        return json.loads(toJSONStr(topMo))
