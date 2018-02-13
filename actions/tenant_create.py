from acitoolkit import acitoolkit as aci
from st2common.runners.base_action import Action


class TenantCreate(Action):
    def run(self, cluster_name, name, description=None):
        config = self.config
        cluster = [cluster for cluster in config['clusters'] if cluster['name'] == cluster_name][0]
        session = aci.Session(cluster['apics'][0], cluster.get('username', config.get('username')), cluster.get('password', config.get('password')))
        session.login()

        tenant = aci.Tenant(name)
        
        if description:
            tenant.desc = description
        
        tenant.push_to_apic(session)
        return True
