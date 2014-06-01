from pyramid.config import Configurator
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

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings, root_factory=root_factory)
    config.include('substanced')
    config.include(pyramid_zcml)
    config.load_zcml("configure.zcml")
    config.scan()
    return config.make_wsgi_app()
