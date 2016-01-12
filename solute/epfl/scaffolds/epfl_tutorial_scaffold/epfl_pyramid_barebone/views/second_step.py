# * encoding: utf-8

from solute import epfl
from solute.epfl import components
from solute.epfl.core.epflassets import EPFLView
from solute.epfl.core.epflassets import ModelBase

from solute.epfl.core.epflcomponentbase import ComponentBase

from .first_step import NoteLayout


class NoteModel(ModelBase):

    data_store = {
        '_id_counter': 1,
        '_id_lookup': {}
    }

    def add_note(self, note):
        note['id'] = self.data_store['_id_counter']
        self.data_store['_id_counter'] += 1
        note.setdefault('children', [])
        note['show_children'] = True
        self.data_store['_id_lookup'][note['id']] = note

        if note['parent']:
            self.get_note(note['parent']).setdefault('children', []).append(note['id'])

    def remove_note(self, note_id):
        parent_id = self.data_store['_id_lookup'].pop(note_id)['parent']
        if parent_id != 0:
            self.get_note(parent_id)['children'].remove(note_id)

    def get_note(self, note_id):
        return self.data_store['_id_lookup'][note_id]

    def set_note(self, note_id, value):
        self.get_note(note_id).update(value)

    def load_notes(self, calling_component, *args, **kwargs):
        # import pprint
        # pprint.pprint(self.data_store)
        # print

        notes_id = calling_component.id
        if notes_id:
            notes = [self.get_note(child_id) for child_id in self.get_note(notes_id)['children']]
        else:
            notes = [note for note in self.data_store['_id_lookup'].values()
                     if not note['parent']]

        print "%s hat folgende children: %s" % (notes_id, notes)
        print
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

        #self.page.notes_link_list.redraw()
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


class NoteBox(components.RecursiveTree):

    pass


class XXXNoteBox(components.Box):
    is_removable = True
    data_interface = {'id': None,
                      'text': None,
                      'children': None,
                      'title': '{title} - ({id})'}

    theme_path = components.Box.theme_path[:]
    theme_path.append('<epfl_pyramid_barebone:templates/theme/note')

    js_parts = components.Box.js_parts[:]
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


class NotesTree(components.RecursiveTree):

    def handle_click_entry(self, *args, **kwargs):
        import ipdb; ipdb.set_trace()

    def handle_click_label(self):
        import ipdb; ipdb.set_trace()


class SecondStepRoot(NoteLayout):

    def init_struct(self):
        self.node_list.extend([
            components.Box(
                title='Edit note',
                node_list=[
                    NoteForm(cid='note_form')]
            ),
            components.RecursiveTree(
                cid='notes_list',
                title='My notes',
                show_children=True,
                get_data='notes',
                data_interface={'id': None, 'label': 'title', 'show_children': None}
            ),
            # components.LinkListLayout(
            #     cid='notes_link_list',
            #     get_data='notes',
            #     show_pagination=False,
            #     show_search=False,
            #     node_list=[
            #         ComponentBase(
            #             url='/',
            #             text='Home'),
            #         ComponentBase(
            #             url='/second',
            #             text='Second',
            #             static_align='bottom')],
            #     data_interface={
            #         'id': None,
            #         'url': 'note?id={id}',
            #         'text': 'title'},
            #     slot='west')
        ])


class ExampleModel(ModelBase):
    data = [
        {'id': i, 'label': 'label %s' % i, 'icon_open': 'icon-open-%s' % i, 'icon_close': 'icon-close-%s' % i}
        for i in range(0, 30)
    ]

    def load_first(self, *args, **kwargs):
        print 'first'
        return self.data[0:10]

    def load_second(self, *args, **kwargs):
        print 'second'
        return self.data[10:20]

    def load_third(self, *args, **kwargs):
        print 'third'
        return self.data[20:30]


@EPFLView(route_name='SecondStep', route_pattern='/second')
class SecondStepPage(epfl.Page):

    root_node = SecondStepRoot()
    # root_node = components.RecursiveTree(
    #     get_data=['first', 'second', 'third'],
    #     show_children=True,
    #     data_interface=[
    #         components.RecursiveTree.data_interface,
    #         components.RecursiveTree.data_interface,
    #         components.RecursiveTree.data_interface
    #     ]
    # )

    model = NoteModel
