import datetime

from acitoolkit import acitoolkit as aci
from _base_aci_sensor import ACISensor


class TenantSensor(ACISensor):
    def setup(self):
        self._logger = self.sensor_service.get_logger(name=self.__class__.__name__)
        self._setup_sessions()
        self._last_refresh = datetime.datetime.utcnow()

        for session in self.aci_sessions.values():
            aci.Tenant.subscribe(session, only_new=True)
    
    def poll(self):
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
        
        time_since_last_refresh = datetime.datetime.utcnow() - self._last_refresh
        if time_since_last_refresh > datetime.timedelta(hours=12):
            # ACI Tokens expire every 24 hours, we're going to refresh ours every 12 just to be safe
            for session in self.aci_sessions.values():
                session.refresh_login()

    def cleanup(self):
        pass

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass
