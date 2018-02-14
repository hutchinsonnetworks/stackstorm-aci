import datetime

from acitoolkit import acitoolkit as aci
from _base_aci_sensor import ACISensor


class TenantSensor(ACISensor):
    def setup(self):
        self._logger = self.sensor_service.get_logger(name=self.__class__.__name__)
        super(TenantSensor, self).setup()

        for session in self.aci_sessions.values():
            aci.Tenant.subscribe(session, only_new=True)
    
    def poll(self):
        super(TenantSensor, self).poll()
        for cluster_name, session in self.aci_sessions.items():
            if aci.Tenant.has_events(session):
                tenant = aci.Tenant.get_event(session)

                trigger = "aci."

                if tenant.is_deleted():
                    trigger += "tenant_deleted"
                else:
                    trigger += "tenant_updated"
                
                self.sensor_service.dispatch(
                    trigger=trigger,
                    payload={
                        "cluster": cluster_name,
                        "name": tenant.name,
                        "dn": tenant.dn,
                        "description": tenant.descr
                    }
                )

    def cleanup(self):
        pass

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass
