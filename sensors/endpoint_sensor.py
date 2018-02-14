import datetime

from acitoolkit import acitoolkit as aci
from _base_aci_sensor import ACISensor


class EndpointSensor(ACISensor):
    def setup(self):
        self._logger = self.sensor_service.get_logger(name=self.__class__.__name__)
        super(EndpointSensor, self).setup()

        for session in self.aci_sessions.values():
            aci.Endpoint.subscribe(session, only_new=True)
    
    def poll(self):
        super(EndpointSensor, self).poll()
        for cluster_name, session in self.aci_sessions.items():
            if aci.Endpoint.has_events(session):
                endpoint = aci.Endpoint.get_event(session)

                trigger = "aci."

                if endpoint.is_deleted():
                    trigger += "endpoint_deleted"
                else:
                    trigger += "endpoint_updated"

                self._logger.info("IP: {}".format(endpoint.ip))
                self._logger.info("MAC: {}".format(endpoint.mac))
                self._logger.info("DN: {}".format(endpoint.dn))
                self._logger.info("EPG: {}".format(endpoint.get_parent().name))
                self._logger.info("Tenant: {}".format(endpoint.get_parent().get_parent().get_parent().name))

                self.sensor_service.dispatch(
                    trigger=trigger,
                    payload={
                        "cluster": cluster_name,
                        "ip": endpoint.ip,
                        "mac": endpoint.mac,
                        "dn": endpoint.dn,
                        "epg": endpoint.get_parent().name,
                        "tenant": endpoint.get_parent().get_parent().get_parent().name
                    }
                )

                self._logger.info("Dispatching trigger {}:".format(trigger))
                self._logger.info({
                    "cluster": cluster_name,
                    "ip": endpoint.ip,
                    "mac": endpoint.mac,
                    "dn": endpoint.dn,
                    "epg": endpoint.get_parent().name,
                    "tenant": endpoint.get_parent().get_parent().get_parent().name
                })

    def cleanup(self):
        pass

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass
