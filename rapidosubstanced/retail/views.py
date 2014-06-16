from pyramid.renderers import get_renderer
from pyramid.view import view_config

from rapido.core.interfaces import IForm

from ..resources import Database, Form


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
    name="opendatabase"
    )
def database_view(context, request):
    return {
        'title': context.title,
        'forms': context.forms,
        'master': get_renderer('templates/master.pt').implementation(),
        }

#
#   "Retail" view for forms.
#
@view_config(
    context=Form,
    renderer='templates/form.pt',
    name="openform"
    )
def form_view(context, request):
    form = IForm(context)
    layout = form.display(edit=True)
    return {
        'title': context.title,
        'id': form.id,
        'layout': layout,
        'master': get_renderer('templates/master.pt').implementation(),
        }

