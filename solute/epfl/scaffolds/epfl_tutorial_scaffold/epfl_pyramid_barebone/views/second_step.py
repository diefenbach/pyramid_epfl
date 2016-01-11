# * encoding: utf-8

from pyramid.view import view_config
from solute import epfl

from solute.epfl.components import Box
from solute.epfl.components import Form
from solute.epfl.components import NumberInput
from solute.epfl.components import TextInput
from solute.epfl.components import Textarea
from solute.epfl.components import Button
from solute.epfl.components import NavLayout

from solute.epfl.components import LinkListLayout

from solute.epfl.core.epflassets import ModelBase
from solute.epfl.core.epflassets import EPFLView
from solute.epfl.core.epflcomponentbase import ComponentBase

from .first_step import FirstStepRoot


class NoteForm(Form):
    node_list = [NumberInput(label='Parent note id',
                          name='parent'),
                 TextInput(label='Title',
                        name='title'),
                 Textarea(label='Text',
                            name='text'),
                 Button(value='Submit',
                          event_name='submit'),
                 Button(value='Cancel',
                          event_name='cancel')]

    compo_state = Form.compo_state + ["id"]
    id = None

    def handle_submit(self):
        if not self.validate():
            self.page.show_fading_message('An error occurred in validating the form!', 'error')
            return
        values = self.get_values()
        note_value = {'parent': values['parent'],
                      'title': values['title'],
                      'text': values['text']}
        if self.id is None:
            self.page.model.add_note(note_value)
        else:
            self.page.model.set_note(self.id, note_value)
        self.clean_form()

    def handle_cancel(self):
        self.clean_form()

    def clean_form(self):
        self.id = None
        self.set_value('title', '')
        self.set_value('text', '')
        self.set_value('parent', 0)
        self.redraw()

    def load_note(self, note_id):
        note = self.page.model.get_note(note_id)
        self.id = note['id']
        self.set_value('parent', note['parent'])
        self.set_value('title', note['title'])
        self.set_value('text', note['text'])
        self.redraw()


class NoteBox(Box):
    is_removable = True
    data_interface = {'id': None,
                      'text': None,
                      'children': None,
                      'title': '{title} - ({id})'}

    theme_path = Box.theme_path[:]
    theme_path.append('<epfl_pyramid_barebone:templates/theme/note')

    js_parts = Box.js_parts[:]
    js_parts.append('epfl_pyramid_barebone:templates/theme/note/note.js')


    def __init__(self, *args, **kwargs):
        super(NoteBox, self).__init__(*args, **kwargs)
        self.get_data = 'note_children'
        self.default_child_cls = NoteBox

    def handle_edit_note(self):
        self.page.note_form.load_note(self.id)

    def handle_removed(self):
        super(NoteBox, self).handle_removed()
        if self.page.note_form.id == self.id:
            self.page.note_form.clean_form()
        self.page.model.remove_note(self.id)


class NoteModel(ModelBase):
    data_store = {'_id_counter': 1,
                  '_id_lookup': {}}

    def add_note(self, note):
        note['id'] = self.data_store['_id_counter']
        self.data_store['_id_counter'] += 1
        note.setdefault('children', [])

        self.data_store['_id_lookup'][note['id']] = note

        if note['parent']:
            self.get_note(note['parent']).setdefault('children', []).append(note['id'])
        else:
            self.data_store.setdefault('notes', []).append(note)

    def remove_note(self, note_id):
        self.data_store['notes'] = [note for note in self.data_store['notes'] if note['id'] != note_id]
        parent_id = self.data_store['_id_lookup'].pop(note_id)['parent']
        if parent_id != 0:
            self.get_note(parent_id)['children'].remove(note_id)

    def get_note(self, note_id):
        return self.data_store['_id_lookup'][note_id]

    def set_note(self, note_id, value):
        self.get_note(note_id).update(value)

    def load_notes(self, calling_component, *args, **kwargs):
        notes = self.data_store.get('notes', [])
        return notes

    def load_note_children(self, calling_component, *args, **kwargs):
        return [self.get_note(child_id) for child_id in self.get_note(calling_component.id)['children']]


class SecondStepRoot(FirstStepRoot):
    def init_struct(self):
        self.node_list.extend([Box(title='Edit note',
                                   node_list=[NoteForm(cid='note_form')]),
                               LinkListLayout(get_data='notes',
                                              show_pagination=False,
                                              show_search=False,
                                              node_list=[ComponentBase(url='/',
                                                                       text='Home'),
                                                         ComponentBase(url='/second',
                                                                       text='Second',
                                                                       static_align='bottom')],
                                              data_interface={'id': None,
                                                              'url': 'note?id={id}',
                                                              'text': 'title'},
                                              slot='west'),
                               Box(title='My notes',
                                   default_child_cls=NoteBox,
                                   data_interface=NoteBox.data_interface,
                                   get_data='notes')])


@EPFLView(route_name='SecondStep', route_pattern='/second')
class SecondStepPage(epfl.Page):
    root_node = SecondStepRoot()
    model = NoteModel
