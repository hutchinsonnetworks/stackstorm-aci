import datetime

from acitoolkit import acitoolkit as aci
from st2reactor.sensor.base import PollingSensor


class ACISensor(PollingSensor):
    def setup(self):
        self._last_refresh = datetime.datetime.utcnow()
        self._setup_sessions()

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

    def poll(self):
        time_since_last_refresh = datetime.datetime.utcnow() - self._last_refresh
        if time_since_last_refresh > datetime.timedelta(seconds=240):
            # ACI Tokens expire every 24 hours, we're going to refresh ours every 12 just to be safe
            # This could actually be incorrect... Some documentation points to every 300 seconds
            self._logger.info("Refreshing APIC Session(s)")
            self._last_refresh = datetime.datetime.utcnow()
            for session in self.aci_sessions.values():
                session.refresh_login()
