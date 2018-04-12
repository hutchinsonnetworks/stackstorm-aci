from _base import AciAction

import cobra.mit.naming
import cobra.mit.request
import cobra.model.l3ext

from cobra.internal.codec.xmlcodec import toXMLStr
from cobra.internal.codec.jsoncodec import toJSONStr

import json


class L3oSviCreate(AciAction):
    def run(self, cluster_name, tenant_name, l3o_name, node_profile_name, interface_profile_name, node_a, node_a_ip, node_b, node_b_ip, node_float_ip, path_name, path_type, vlan_id, mtu='inherit'):

        # connect to apic
        md = self._login(cluster_name)

        if path_type == "vpc":
            # the top level object on which operations will be made
            topDn = cobra.mit.naming.Dn.fromString('uni/tn-' + tenant_name + '/out-' + l3o_name + "/lnodep-" + node_profile_name + "/lifp-" + interface_profile_name + "/rspathL3OutAtt-[topology/pod-1/protpaths-" + node_a + "-" + node_b + "/pathep-[" + path_name + "]]")

            topParentDn = topDn.getParent()
            topMo = md.lookupByDn(topParentDn)

            # build the request using cobra syntax
            l3extRsPathL3OutAtt = cobra.model.l3ext.RsPathL3OutAtt(topMo,
                addr='0.0.0.0',
                descr='',
                encapScope='local',
                targetDscp='unspecified',
                llAddr='::',
                #mac='00:22:BD:F8:19:FF' #Let the mac be dynamic from ACI,
                mode='regular',
                encap='vlan-' + vlan_id,
                ifInstT='ext-svi',
                mtu=mtu,
                tDn='topology/pod-1/protpaths-' + node_a + '-' + node_b + '/pathep-[' + path_name + ']')


            l3extMember = cobra.model.l3ext.Member(l3extRsPathL3OutAtt, name='', descr='', llAddr='::', nameAlias='', side='A', addr=node_a_ip)
            l3extIp = cobra.model.l3ext.Ip(l3extMember, nameAlias='', addr=node_float_ip, descr='', name='')
            l3extMember2 = cobra.model.l3ext.Member(l3extRsPathL3OutAtt, name='', descr='', llAddr='::', nameAlias='', side='B', addr=node_b_ip)
            l3extIp2 = cobra.model.l3ext.Ip(l3extMember2, nameAlias='', addr=node_float_ip, descr='', name='')

        # commit the generated code to APIC
        c = cobra.mit.request.ConfigRequest()
        c.addMo(topMo)
        md.commit(c)

        return json.loads(toJSONStr(topMo))
