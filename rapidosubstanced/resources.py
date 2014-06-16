import colander
import deform.widget
from persistent import Persistent

from pyramid.threadlocal import get_current_request
from pyramid.traversal import resource_path

from substanced.content import content
from substanced.property import PropertySheet
from substanced.schema import (
    Schema,
    NameSchemaNode
    )
from substanced.util import renamer, set_oid, get_oid
from substanced.util import find_catalog
from substanced.folder import Folder

from zope.interface import implements
from zope.annotation.interfaces import IAttributeAnnotatable
from rapido.core.interfaces import IDatabasable, IFormable, IForm
from rapido.core.interfaces import IImporter

def context_is_a_form(context, request):
    return request.registry.content.istype(context, 'Form')

class FormSchema(Schema):
    name = NameSchemaNode(
        editing=context_is_a_form,
        )
    title = colander.SchemaNode(
        colander.String(),
        )

class FormPropertySheet(PropertySheet):
    schema = FormSchema()

@content(
    'Form',
    icon='glyphicon glyphicon-align-left',
    add_view='add_form',
    propertysheets=(
        ('Basic', FormPropertySheet),
        ),
    )
class Form(Persistent):
    implements(IAttributeAnnotatable, IFormable)

    name = renamer()

    def __init__(self, id, title=''):
        self.id = id
        self.title = title

    @property
    def path(self):
        return resource_path(self)


def context_is_a_database(context, request):
    return request.registry.content.istype(context, 'Database')

class DatabaseSchema(Schema):
    name = NameSchemaNode(
        editing=context_is_a_database,
        )
    title = colander.SchemaNode(
        colander.String(),
        )

class DatabasePropertySheet(PropertySheet):
    schema = DatabaseSchema()

@content(
    'Database',
    icon='glyphicon glyphicon-align-left',
    add_view='add_database',
    propertysheets=(
        ('Basic', DatabasePropertySheet),
        ),
    )
class Database(Folder):
    implements(IAttributeAnnotatable, IDatabasable)

    name = renamer()

    def __init__(self, title=''):
        Folder.__init__(self)
        self.title = title
        
    def create_form(self, settings, code, html):
        form_id = settings['id']
        self[form_id] = Form(form_id, settings['title'])
        form_obj = self[form_id]
        form = IForm(form_obj)
        form.assign_rules(settings['assigned_rules'])
        form.set_code(code)
        form.set_layout(html)
        for (field_id, field_settings) in settings['fields'].items():
            form.set_field(field_id, {
                'type': field_settings['type'],
                'index_type': field_settings.get('index_type', ''),
            })

    def current_user(self):
        return get_current_request().user.__name__

    def current_user_groups(self):
        return [group.__name__ for group in get_current_request().user.groups]

    @property
    def uid(self):
        return get_oid(self)

    @property
    def path(self):
        return resource_path(self)

    @property
    def root(self):
        return self.__parent__

    @property
    def forms(self):
        catalog = find_catalog(self, 'system')
        content_type = catalog['content_type']
        path = catalog['path']
        q = content_type.eq('Form') & path.eq(self.path)
        return q.execute()