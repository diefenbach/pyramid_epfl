# * encoding: utf-8

from solute import epfl
from solute.epfl.core.epflcomponentbase import ComponentBase
from solute.epfl.components import Box
from solute.epfl.components import Text
from solute.epfl.components import PlainHtml
from solute.epfl.components import Form
from solute.epfl.components import TextInput
from solute.epfl.components import Textarea
from solute.epfl.components import Button
from solute.epfl.components import NavLayout
from solute.epfl.components import LinkListLayout

from solute.epfl.core.epflassets import EPFLView
from solute.epfl.core.epflassets import ModelBase


class NoteForm(Form):

    node_list = [TextInput(label='Title',
                           name='title',
                           mandatory=True,
                           placeholder='Insert a title here!'),
                 Textarea(label='Text',
                          mandatory=True,
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
        note_value = {'title': values['title'],
                      'text': values['text']}

        if self.id is None:
            self.page.model.add_note(note_value)
        else:
            self.page.model.set_note(self.id, note_value)

        #self.page.notes_link_list.redraw()
        self.page.notes_list.redraw()
        self.clean_form()

    def handle_cancel(self):
        self.clean_form()

    def clean_form(self):
        self.id = None
        self.set_value('title', '')
        self.set_value('text', '')
        self.redraw()

    def load_note(self, note_id):
        note = self.page.model.get_note(note_id)
        self.id = note['id']
        self.set_value('title', note['title'])
        self.set_value('text', note['text'])
        self.redraw()


class NoteBox(Box):

    is_removable = True
    #disable_auto_update = True

    def init_struct(self):

        # self.node_list.append(ComponentBase(template_name='epfl_pyramid_barebone:templates/note.html'))
        # self.node_list.append(Button(value='Edit this note',
        #                              event_name='edit_note'))
        self.node_list.append(Text(value=self.reflect.container_compo.text))
        self.node_list.append(Button(value='Edit this note',
                                     event_name='edit_note'))

    def handle_edit_note(self):
        self.page.note_form.load_note(self.id)

    def handle_removed(self):
        super(NoteBox, self).handle_removed()
        if self.page.note_form.id == self.id:
            self.page.note_form.clean_form()

        self.page.model.remove_note(self.id)


class NoteModel(ModelBase):

    data_store = {'_id_counter': 1}

    def add_note(self, note):
        note['id'] = self.data_store['_id_counter']
        self.data_store['_id_counter'] += 1
        self.data_store.setdefault('notes', []).append(note)

    def remove_note(self, note_id):
        self.data_store['notes'] = [note for note in self.data_store['notes'] if note['id'] != note_id]

    def get_note(self, note_id):
        return [note for note in self.data_store['notes'] if note['id'] == note_id][0]

    def set_note(self, note_id, value):
        self.get_note(note_id).update(value)

    def load_notes(self, calling_component, *args, **kwargs):
        return self.data_store.get('notes', [])


class FirstStepRoot(epfl.components.CardinalLayout):

    constrained = True

    node_list = [NavLayout(slot='north',
                           # links=[('Second Step', '/second'),
                           #        ('Third Step', '/third'),
                           #        ('Fourth Step', '/fourth')],
                           title='Demo Notes App')]

    def init_struct(self):

        self.node_list.extend([Box(title='Edit note',
                                   node_list=[NoteForm(cid='note_form')]),
                               Box(cid='notes_list',
                                   title='My notes',
                                   default_child_cls=NoteBox,
                                   data_interface={'id': None,
                                                   'text': None,
                                                   'title': None},
                                   get_data='notes')])

        # self.node_list.extend([Box(title='Edit note',
        #                            node_list=[NoteForm(cid='note_form')]),
        #                        Box(cid="notes_list",
        #                            title='My notes',
        #                            default_child_cls=NoteBox,
        #                            data_interface={'id': None,
        #                                            'text': None,
        #                                            'title': None},
        #                            get_data='notes'),
        #                        LinkListLayout(cid="notes_link_list",
        #                                       slot='west',
        #                                       auto_update_children=True,
        #                                       show_pagination=False,
        #                                       show_search=False,
        #                                       get_data='notes',
        #                                       data_interface={'id': None,
        #                                                       'url': 'note?id={id}',
        #                                                       'text': 'title'}
        #                                       )])


@EPFLView(route_name='FirstStep', route_pattern='/')
class FirstStepPage(epfl.Page):
    root_node = FirstStepRoot()
    model = NoteModel
