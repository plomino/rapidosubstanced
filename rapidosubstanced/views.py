from pyramid.httpexceptions import HTTPFound

from substanced.sdi import mgmt_view
from substanced.form import FormView
from substanced.interfaces import IFolder

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
        
        # TEST
        importer = IImporter(db)
        importer.import_database({'forms': {'frmBook': {'frmBook.py': "\ndef forever(context):\n    return 'I will never change.'", 'frmBook.yaml': 'assigned_rules: [polite]\nfields:\n  author: {index_type: text, type: TEXT}\n  famous_quote: {mode: COMPUTED_ON_SAVE, type: TEXT}\n  forever: {mode: COMPUTED_ON_CREATION, type: TEXT}\nid: frmBook\ntitle: Book form\n', 'frmBook.html': 'Author: <span data-rapido-field="author">author</span>'}}, 'settings.yaml': 'acl:\n  rights:\n    author: [FamousDiscoverers]\n    editor: []\n    manager: [admin]\n    reader: []\n  roles: {}\n'})

        return HTTPFound(
            self.request.sdiapi.mgmt_path(self.context, '@@contents')
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