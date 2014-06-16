from pyramid.renderers import get_renderer, render_to_response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from rapido.core.interfaces import IForm, IDatabase

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

@view_config(
    context=Database,
    name="document",
    )
def get_document(context, request):
    path = request.path.split('/')
    if path[-1] == 'edit':
        docid = path[-2]
    elif path[-1] == 'save':
        docid = path[-2]
    else:
        docid = path[-1]
    doc = IDatabase(context).get_document(docid)
    return render_to_response(
        "templates/opendocument.pt",
        {
            'title': doc.title,
            'body': doc.display(),
            'master': get_renderer('templates/master.pt').implementation(),
        },
        request)



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

@view_config(
    context=Form,
    name="create",
    request_method="POST",
    )
def create(context, request):
    form = IForm(context)
    doc = form.database.create_document()
    doc.set_item('Form', form.id)
    doc.save(request.params, form=form, creation=True)
    return HTTPFound(
        location=doc.url
        )