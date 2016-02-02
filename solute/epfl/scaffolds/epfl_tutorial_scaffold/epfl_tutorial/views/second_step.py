# * encoding: utf-8

from solute import epfl
from solute.epfl import components
from solute.epfl.core.epflassets import EPFLView
from solute.epfl.core.epflassets import ModelBase

from .first_step import NoteLayout


class NoteModel(ModelBase):
    """ Simplified recursive model without edit and remove. Just adding and getting
    is handled. """

    data_store = {
        '_id_counter': 1,
        '_id_lookup': {}
    }

    def add_note(self, note):
        note['id'] = self.data_store['_id_counter']
        self.data_store['_id_counter'] += 1
        note.setdefault('children', [])
        note['show_children'] = True
        note['icon_open'] = 'plus-square-o'
        note['icon_close'] = 'minus-square-o'
        self.data_store['_id_lookup'][note['id']] = note

        if note['parent']:
            self.get_note(note['parent']).setdefault('children', []).append(note['id'])

    def get_note(self, note_id):
        return self.data_store['_id_lookup'][note_id]

    def load_notes(self, calling_component, *args, **kwargs):
        notes_id = getattr(calling_component, 'id', None)
        if notes_id:
            notes = [self.get_note(child_id) for child_id in self.get_note(notes_id)['children']]
        else:
            notes = [note for note in self.data_store['_id_lookup'].values()
                     if not note['parent']]

        return notes


class NoteForm(components.Form):

    id = None
    compo_state = components.Form.compo_state + ["id"]

    node_list = [
        components.NumberInput(
            label='Parent note id',
            name='parent'),
        components.TextInput(
            label='Title',
            name='title',
            mandatory=True,
            placeholder='Insert a title here!'),
        components.Textarea(
            label='Text',
            name='text',
            mandatory=True),
        components.Button(
            value='Submit',
            color='primary',
            event_name='submit'),
        components.Button(
            value='Cancel',
            event_name='cancel')
    ]

    def handle_submit(self):
        if not self.validate():
            self.page.show_fading_message(
                'An error occurred in validating the form!', 'error'
            )
            return

        note_value = self.get_values()
        if note_value['parent']:
            # force integer ids
            note_value['parent'] = int(note_value['parent'])
        if self.id is None:
            self.page.model.add_note(note_value)
        else:
            self.page.model.set_note(self.id, note_value)

        self.page.notes_link_list.redraw()
        self.page.notes_list.redraw()
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


class SecondStepRoot(NoteLayout):

    def init_struct(self):
        self.node_list.extend([
            components.Box(
                title='Edit note',
                node_list=[NoteForm(cid='note_form')]
            ),
            components.Box(
                cid='notes_list_box',
                title='My notes tree',
                node_list=[components.RecursiveTree(
                    cid='notes_list',
                    show_children=True,
                    get_data='notes',
                    disable_auto_update=True,
                    data_interface={'id': None, 'label': 'title', 'show_children': None,
                                    'icon_open': None, 'icon_close': None}
                    )]
            ),
            components.LinkListLayout(
                cid="notes_link_list",
                slot='west',
                auto_update_children=True,
                show_pagination=False,
                show_search=False,
                get_data='notes',
                event_name='open_details',
                data_interface={
                    'id': None,
                    'url': 'note/{id}',
                    'text': 'title'}
            )
        ])

    def handle_open_details(self):
        """ Handler to open a modal with some note details, triggered via click on the
        LinkListLayout entries in the west slot. """
        calling_cid = self.epfl_event_trace[0]
        note_id = self.page.components[calling_cid].id
        note_data = self.page.model.get_note(note_id)

        self.add_component(
            components.ModalBox(
                cid='note_detail_box',
                title='Note Details',
                node_list=[
                    components.Text(
                        tag='h3',
                        verbose=True,
                        value=note_data['title']),
                    components.Text(
                        value=note_data['text'])]
                )
            )
        self.redraw()


@EPFLView(route_name='SecondStep', route_pattern='/second')
class SecondStepPage(epfl.Page):

    root_node = SecondStepRoot()
    model = NoteModel
