from pyramid.renderers import get_renderer
from pyramid.view import view_config
from ..resources import Database

#
#   Default "retail" view
#
@view_config(
    renderer='templates/splash.pt',
    )
def splash_view(request):
    manage_prefix = request.registry.settings.get('substanced.manage_prefix',
                                                  '/manage')
    return {'manage_prefix': manage_prefix}

#
#   "Retail" view for databases.
#
@view_config(
    context=Database,
    renderer='templates/database.pt',
    )
def database_view(context, request):
    return {'title': context.title,
            'body': context.body,
            'master': get_renderer('templates/master.pt').implementation(),
           }

