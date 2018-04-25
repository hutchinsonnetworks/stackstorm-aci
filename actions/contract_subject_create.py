from _base import AciAction
import json


class ContractSubjectCreate(AciAction):
    def run(self, cluster_name, tenant_name, contract_name, name, reverse_filter_ports=False, filter_name=None):
        from cobra.internal.codec.jsoncodec import toJSONStr

        import cobra.mit.naming
        import cobra.mit.request
        import cobra.model.vz

        # connect to apic
        md = self._login(cluster_name)

        # the top level object on which operations will be made
        topParentDn = cobra.mit.naming.Dn.fromString('uni/tn-' + tenant_name + '/brc-' + contract_name)
        topMo = md.lookupByDn(topParentDn)

        if reverse_filter_ports:
            revFltPorts = 'yes'
        else:
            revFltPorts = 'no'

        # build the request using cobra syntax
        vzSubj = cobra.model.vz.Subj(topMo, revFltPorts=revFltPorts, name=name, prio='unspecified', targetDscp='unspecified', nameAlias='', descr='', consMatchT='AtleastOne', provMatchT='AtleastOne')

        if filter_name is not None:
            vzRsSubjFiltAtt = cobra.model.vz.RsSubjFiltAtt(vzSubj, directives='', tnVzFilterName=filter_name)

        # commit the generated code to APIC
        c = cobra.mit.request.ConfigRequest()
        c.addMo(topMo)
        md.commit(c)

        return json.loads(toJSONStr(topMo))
