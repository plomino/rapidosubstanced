import json

from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

import colander
import deform.widget

from substanced.sdi import mgmt_view
from substanced.form import FormView
from substanced.interfaces import IFolder
from substanced.schema import Schema

from rapido.core.interfaces import IDatabase, IImporter

from .resources import DatabaseSchema, FormSchema

#
#   SDI "add" view for databases
#
@mgmt_view(
    context=IFolder,
    name='add_database',
    tab_title='Add Database',
    permission='sdi.add-content',
    renderer='substanced.sdi:templates/form.pt',
    tab_condition=False,
    )
class AddDatabaseView(FormView):
    title = 'Add Database'
    schema = DatabaseSchema()
    buttons = ('add',)

    def add_success(self, appstruct):
        registry = self.request.registry
        name = appstruct.pop('name')
        database = registry.content.create('Database', **appstruct)
        self.context[name] = database
        db = IDatabase(database)
        db.initialize()
        db.storage.soup
        
        return HTTPFound(
            self.request.sdiapi.mgmt_path(self.context, '@@contents')
            )

class ImportSchema(Schema):
    json_design = colander.SchemaNode(
        colander.String(),
        widget = deform.widget.TextAreaWidget(rows=10, cols=120),
        title='Design as JSON',
        )

@mgmt_view(
    content_type='Database',
    name="import_export",
    tab_title="Import/export",
    permission='sdi.add-content',
    renderer='templates/importexport.pt',
    )
class ImportExportView(FormView):
    schema = ImportSchema(title='Import')
    buttons = ('import',)

    def import_success(self, data):
        db = IDatabase(self.context)
        importer = IImporter(db)
        importer.import_database(json.loads(data['json_design']))
        return HTTPFound(
            location=self.request.sdiapi.mgmt_path(self.context, '@@contents')
            )


@mgmt_view(
    content_type='Database',
    name='add_form',
    tab_title='Add Form',
    permission='sdi.add-content',
    renderer='substanced.sdi:templates/form.pt',
    tab_condition=False,
    )
class AddFormView(FormView):
    title = 'Add Form'
    schema = FormSchema()
    buttons = ('add',)

    def add_success(self, appstruct):
        registry = self.request.registry
        name = appstruct.pop('name')
        form = registry.content.create('Form', **appstruct)
        self.context[name] = form
        return HTTPFound(
            self.request.sdiapi.mgmt_path(self.context, '@@contents')
            )