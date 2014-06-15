from pyramid.config import Configurator
from zope.component import getGlobalSiteManager
import pyramid_zcml

from substanced.db import root_factory

# from zope.configuration.xmlconfig import XMLConfig
# import zope.component
# XMLConfig("meta.zcml", zope.component)()
# import zope.annotation
# XMLConfig("configure.zcml", zope.annotation)()
# import rapido.core
# XMLConfig("configure.zcml", rapido.core)()
# import rapido.souper
# XMLConfig("configure.zcml", rapido.souper)()

class RegistryWrapper(dict):
    """ Substance D expects an actual Pyramid Registry. As we need to use ZCA,
    we wrap the globalreg so it acts as a dict (just like the Pyramid Registry)
    """
    def __init__(self, reg):
        self.reg = reg

    def __getattr__(self,attr):
        return getattr(self.reg, attr)

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    # config = Configurator(settings=settings, root_factory=root_factory)
    globalreg = getGlobalSiteManager()
    config = Configurator(registry=RegistryWrapper(globalreg))
    config.setup_registry(settings=settings)
    config.set_root_factory(root_factory)
    config.include('substanced')
    config.include(pyramid_zcml)
    config.load_zcml("configure.zcml")
    config.scan()
    return config.make_wsgi_app()
