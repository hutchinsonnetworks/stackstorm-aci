from acitoolkit import acitoolkit as aci
from st2reactor.sensor.base import PollingSensor


class ACISensor(PollingSensor):
    def _setup_sessions(self):
        self._logger = self.sensor_service.get_logger(name=self.__class__.__name__)
        self._logger.info("Setting up Sessions")

        config = self.config

        self.aci_sessions = {}
        for cluster in config['clusters']:
            name = cluster['name']
            apics = cluster['apics']
            self.aci_sessions[name] = aci.Session(
                apics[0],       # TODO: Make this smarter - select working APIC
                cluster.get('username', config.get('username')),
                cluster.get('password', config.get('password'))
            )
            self.aci_sessions[name].login()
