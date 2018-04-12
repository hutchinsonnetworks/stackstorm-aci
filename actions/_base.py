from st2common.runners.base_action import Action
import pkg_resources

class AciAction(Action):
    def __init__(self, config):
        super(AciAction, self).__init__(config)

        location = config['cobra']['download_location']
        acicobra = config['cobra']['eggs']['cobra']
        acimodel = config['cobra']['eggs']['model']

        current_module_set = pkg_resources.WorkingSet()

        #Check for ACICOBRA and install if needed
        try:
            current_module_set.require('acicobra')
        except:
            from setuptools.command import easy_install

            easy_install.main( ["-U",location + acicobra] )
            pkg_resources.require('acicobra')

        #Check for ACIMODEL and install if needed
        try:
            current_module_set.require('acimodel')
        except:
            from setuptools.command import easy_install

            easy_install.main( ["-U",location + acimodel] )
            pkg_resources.require('acimodel')


    def _login(self, cluster_name):
        from cobra.mit.access import MoDirectory
        from cobra.mit.session import LoginSession

        config = self.config
        cluster = [cluster for cluster in config['clusters'] if cluster['name'] == cluster_name][0]

        # log into an APIC and create a directory object
        session = LoginSession(cluster['apics'][0], config.get('username'), config.get('password'), requestFormat="json")
        moDir = MoDirectory(session)
        moDir.login()

        if type(moDir) is MoDirectory:
            return moDir
        else:
            raise()
