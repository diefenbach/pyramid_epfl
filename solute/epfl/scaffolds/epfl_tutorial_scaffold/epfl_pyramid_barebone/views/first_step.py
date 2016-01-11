# * encoding: utf-8

from solute import epfl
from solute.epfl import components
from solute.epfl.core.epflassets import EPFLView
from solute.epfl.core.epflassets import ModelBase


class NoteModel(ModelBase):
    """ The model handles storage and reading of data. In this example, a simple
    memory based dict is used for the sake of simplicity. """

    data_store = {'_id_counter': 1}

    def add_note(self, note):
        note['id'] = self.data_store['_id_counter']
        self.data_store['_id_counter'] += 1
        self.data_store.setdefault('notes', []).append(note)

    def remove_note(self, note_id):
        self.data_store['notes'] = [
            note for note in self.data_store['notes'] if note['id'] != note_id
        ]

    def get_note(self, note_id):
        return [note for note in self.data_store['notes'] if note['id'] == note_id][0]

    def set_note(self, note_id, value):
        self.get_note(note_id).update(value)

    def load_notes(self, calling_component, *args, **kwargs):
        return self.data_store.get('notes', [])


class NoteForm(components.Form):

    id = None
    compo_state = components.Form.compo_state + ["id"]

    node_list = [
        components.TextInput(
            label='Title',
            name='title',
            mandatory=True,
            placeholder='Insert a title here!'),
        components.Textarea(
            label='Text',
            mandatory=True,
            name='text'),
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
        self.redraw()

    def load_note(self, note_id):
        note = self.page.model.get_note(note_id)
        self.id = note['id']
        self.set_value('title', note['title'])
        self.set_value('text', note['text'])
        self.redraw()


class NoteLayout(components.CardinalLayout):

    plain = ['north']
    constrained = True
    node_list = [
        components.NavLayout(
            slot='north',
            title='Epfl Tutorial App',
            node_list=[
                components.Link(
                    text='First step',
                    url='/',
                    slot='right'),
                components.Link(
                    text='Second step',
                    url='/second',
                    slot='right'),
                components.Link(
                    text='Third step',
                    url='/third',
                    slot='right')]
        )]


class FirstStepRoot(NoteLayout):

    def init_struct(self):
        self.node_list.extend([
            components.Box(
                title='Edit note',
                node_list=[NoteForm(cid='note_form')]
            ),
            components.Box(
                cid="notes_list",
                title='My notes',
                default_child_cls=components.Box(
                    node_list=[
                        components.Text(value=self.reflect.container_compo.text),
                        components.ColLayout(
                            node_list=[
                                components.Button(
                                    value='Edit this note',
                                    color='primary',
                                    cols=6,
                                    event_name='edit_note'),
                                components.Button(
                                    value='Delete this note',
                                    color='danger',
                                    cols=6,
                                    event_name='delete_note')]
                        )]
                ),
                data_interface={
                    'id': None,
                    'text': None,
                    'title': None},
                get_data='notes'),
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

    def handle_edit_note(self):
        calling_cid = self.epfl_event_trace[0]
        note_id = self.page.components[calling_cid].container_compo.container_compo.id
        self.page.note_form.load_note(note_id)

    def handle_delete_note(self):
        calling_cid = self.epfl_event_trace[0]
        note_id = self.page.components[calling_cid].container_compo.container_compo.id

        if self.page.note_form.id == note_id:
            self.page.note_form.clean_form()

        self.page.model.remove_note(note_id)


@EPFLView(route_name='FirstStep', route_pattern='/')
class FirstStepPage(epfl.Page):

    root_node = FirstStepRoot()
    model = NoteModel
