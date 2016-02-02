.. _tutorial_2:

Tutorial Part 2: Notes App with nested notes
============================================

In part 2 of the tutorial, we continue with the notes app we have created in part 1.
But as it slightly differs, we use a new page for it. To do so, we first need to add a new file called 'second_step.py' in the views folder of our demo app.

Add the following skeleton to it:

.. code-block:: python

    # * encoding: utf-8

    from solute import epfl
    from solute.epfl import components
    from solute.epfl.core.epflassets import EPFLView
    from solute.epfl.core.epflassets import ModelBase

    from .first_step import NoteLayout


    class SecondStepRoot(NoteLayout):

        pass


    @EPFLView(route_name='SecondStep', route_pattern='/second')
    class SecondStepPage(epfl.Page):

        root_node = SecondStepRoot()


The first thing you will notice after starting pyramid is: it won't start. This is caused by an EPFL check: every page must also be defined as an active module for epfl. This is done be extending the 'epfl.active_modules' list of your wsgi config for pyramid. So open the development.ini file in your projekt root and extend the line like this:

.. code-block:: ini

    epfl.active_modules = epfl_starter.views.first_step
                          epfl_starter.views.second_step


After this change and start of pyramid you access the url http://localhost:8080/second which displays the empty page with title, as known from the start of the first step.

In this part, we will extend our notes app with nested notes, that means a note can have multiple child notes which can itself have child notes, and so on.
For this, we can specify the parent id of a note when creating or editing it, and the notes list displays nested notes in a tree-like view.

Let's start by adapting our NoteModel to reflect child notes:

.. code-block:: python

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

Note, that this model is simplified by reducing it to functionality to just add and display notes. Editing and removing is not covered here and not used later on.

As always, we set the Model as attribute to our page:

.. code-block:: python

    @EPFLView(route_name='SecondStep', route_pattern='/second')
    class SecondStepPage(epfl.Page):

        root_node = SecondStepRoot()
        model = NoteModel


Note that we've added the parameter calling_component to the load_note_children() method.
We need this later because this method, being prefixed with "load_", will serve later for a component to obtain note children via
the get_data attribute. When this method is called then, the calling_component parameter can be used to obtain the component that has
called, and obtain the note children for the calling components note.

Up to now, nothing has changed in our page. So let's add the form known from step one again and extend it by a new input to enter the parent's id of a note.

.. code-block:: python

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

Now for the fun part.

We now extend our NoteBox to display nested notes.

Up to now, Notes were listed in a Box using default_child_cls, and it directly renders the contents of a single note via another box.

To display a tree of notes, the RecursiveTree component is used. Replace the notes_list component like this:

.. code-block:: python

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

This is enough to complete the second step of our tutorial. Just replace one component with another to display recursive data.

The only thing missing here, is the event handler method for the open_details event of the notes_link_list which can be copied from step one over here. It's up to you if you want to.

In the next step, we create a simple login dialog to demonstrate rights management in EPFL. You can have a look of the complete file of this step at https://github.com/solute/pyramid_epfl/blob/master/solute/epfl/scaffolds/epfl_tutorial_scaffold/epfl_tutorial/views/second_step.py
