from _base import AciAction
import json


class ApEpgCreate(AciAction):

    def run(self, cluster_name, tenant_name, ap_name, name, bd_name=None):
        from cobra.internal.codec.jsoncodec import toJSONStr

        import cobra.mit.naming
        import cobra.mit.request
        import cobra.model.fv

        # connect to apic
        md = self._login(cluster_name)

        # the top level object on which operations will be made
        topParentDn = cobra.mit.naming.Dn.fromString('uni/tn-' + tenant_name + '/ap-' + ap_name)
        topMo = md.lookupByDn(topParentDn)

        # build the request using cobra syntax
        fvAEPg = cobra.model.fv.AEPg(topMo, isAttrBasedEPg='no', matchT='AtleastOne', name=name, descr='', fwdCtrl='', prefGrMemb='exclude', nameAlias='', prio='unspecified', pcEnfPref='unenforced')

        fvRsCustQosPol = cobra.model.fv.RsCustQosPol(fvAEPg, tnQosCustomPolName='')

        if bd_name is not None:
            fvRsBd = cobra.model.fv.RsBd(fvAEPg, tnFvBDName=bd_name)


# commit the generated code to APIC
        c = cobra.mit.request.ConfigRequest()
        c.addMo(topMo)
        md.commit(c)

        return json.loads(toJSONStr(topMo))
