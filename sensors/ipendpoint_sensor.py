import datetime

from acitoolkit import acitoolkit as aci
from _base_aci_sensor import ACISensor


class IPEndpointSensor(ACISensor):
    def setup(self):
        self._logger = self.sensor_service.get_logger(name=self.__class__.__name__)
        super(IPEndpointSensor, self).setup()

        for session in self.aci_sessions.values():
            aci.IPEndpoint.subscribe(session, only_new=True)

    def poll(self):
        super(IPEndpointSensor, self).poll()
        for cluster_name, session in self.aci_sessions.items():
            if aci.IPEndpoint.has_events(session):
                endpoint = aci.IPEndpoint.get_event(sess)
                epg = endpoint.get_parent()
                app_profile = epg.get_parent()
                tenant = app_profile.get_parent()

                trigger = "aci."

                if endpoint.is_deleted():
                    trigger += "ipendpoint_deleted"
                else:
                    trigger += "ipendpoint_updated"
                
                epg = endpoint.get_parent()

                payload = {
                    "cluster": cluster_name,
                    "ip": endpoint.ip,
                    "mac": endpoint.mac,
                    "dn": endpoint.dn,
                    "epg": epg.name,
                    "tenant": epg.get_parent().get_parent().name
                }

                self._logger.info("Dispatching trigger {}:".format(trigger))
                self._logger.info(payload)

                if isinstance(epg, aci.EPG):
                    deep_tenant = aci.Tenant.get_deep(session, names=(tenant.name,), limit_to=["fvTenant", "fvBD", "fvAEPg", "fvCtx"])[0]
                    searcher = aci.Search()
                    searcher.name = epg.name
                    deep_epg = filter(lambda epg: isinstance(epg, aci.EPG), deep_tenant.find(searcher))[0]
                    bridge_domain = deep_epg.get_bd()
                    if bridge_domain is not None:
                        payload['bridge_domain'] = bridge_domain.name

                        vrf = bridge_domain.get_context()
                        payload['vrf'] = vrf.name

                self.sensor_service.dispatch(trigger=trigger, payload=payload)

    def cleanup(self):
        pass

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass
