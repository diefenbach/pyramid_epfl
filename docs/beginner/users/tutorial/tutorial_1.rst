.. _tutorial_1:

Tutorial Part 1: Basic Notes App
================================

In this tutorial, we create a simple EPFL app that provides a simple functionality to create, edit and delete notes.
For this reason, the app simply provides one view, which is by the way a rather common use case in EPFL apps.

First, we start by creating and setting up the app based on an empty EPFL starter pyramid scaffold.
We create the demo app, run setup.py to set it up, and launch it using the pserve command. Make sure you have a (idally virtualenv-based) environment with pyramid_epfl installed.


.. code-block:: bash

    pcreate -s pyramid_epfl_starter demo_app
    cd demo_app/
    python setup.py develop
    pserve development.ini --reload

The app is now running on localhost:8080. If you open the URL, you will see a simple empty page displaying the app
name with some links. We will now extend this app to add the notes functionality.

You can view the final results of the complete tutorial in a different scaffold. Note that you should use a different
virtualenv environment for it.

.. code-block:: bash

    pcreate -s pyramid_epfl_tutorial tutorial_app
    cd tutorial_app/
    python setup.py develop
    pserve development.ini --reload

If you want to view both the final tutorial app and your working version (demo_app), change the port in the
development.ini file of the tutorial app to run both server instances in parallel on your machine.

Let's go back to our empty notes app. In demo_app/epf_starter/views/first_step.py, we will do most of the work.

In this file we already added a navbar to the root component. The root component is the component that
resides directly on the page and is basically responsible for the overall layout of the page.

In first_step.py, we see that the root component is instantiated as follows:

.. code-block:: python

    @EPFLView(route_name='FirstStep', route_pattern='/')
        class FirstStepPage(epfl.Page):
            root_node = FirstStepRoot()

Each page needs a root_node. In this case we defined a class FirstStepRoot, which is derived from
components.CardinalLayout. This component provides a base layout skeleton where child components can define the slot, they are displayed in.

.. code-block:: python

    # define the list of sub components used in this component
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

As first child, we use a components.NavLayout that displays a navbar with title and some links, that are defined in the node_list.
Note that by setting slot="north" in the NavLayout component, we told EPFL that this component is going to be placed in the
top area of the parent component (this is possible since NoteLayout inherits from CardinalLayout which provides this functionality). Later, if there are more components, try to change the slot parameter to 'west' or 'east' to see how this parameter effects the generated layout.

A lot of EPFL's components are so-called container components. They support nested components that are stored in the component's node_list attribute.

Next, we will add some components to the root component: the component that will display the form where we can create a new note or
edit an existing one.
We could do this by just extending node_list with further components when instantiating the FirstStepRoot class, or
by extending the HomeRoot
class itself. We choose the latter way by implementing the init_struct method and extending the node_list.

.. code-block:: python

   def init_struct(self):
        self.node_list.extend([
            components.Box(
                title='Edit note',
                node_list=[
                    components.Form(
                        cid='notes_form'
                    )
                ]
            )
        ])

We have now added a Box to the page that contains an empty form.

Now it's time to fill the form with live. We add form components to the form by extending its node_list:


.. code-block:: python

    def init_struct(self):
        self.node_list.extend([
            components.Box(
                title='Edit note',
                node_list=[
                    components.Form(
                        cid='notes_form',
                        node_list=[
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
                                event_name='submit')
                        ]
                    )
                ]
            )
        ])


If you take a look at the rendered page now, you can already see the form with its fields and the submit button. Neat!

Note that you can already experience the server-side state that EPFL provides: If you enter text in the form and click your
browser's refresh button, the values of the form are kept.

As a next step, we want to handle the event when the user clicks on the submit button. You can add event handling methods to any component.
Ultimatively, we want to handle this event on our Form, since we have to react on the event and create a new note with the values of the form's fields.

Currently, the event when clicking the button is bubbled up the form. Neither the button nor the form provide an event currently, so let's add
event handling functionality to the form.
The easiest way to handle this event is by using an inherited class from Form and use this in the FirstStepRoot.

.. code-block:: python

    class NoteForm(components.Form):
        """ This component displays the form to add and edit note entries. """

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
                event_name='submit')
        ]

    class FirstStepRoot(NoteLayout):

        def init_struct(self):
            self.node_list.extend([
                components.Box(
                    title='Edit note',
                    node_list=[
                        NoteForm(cid='notes_form')
                        ]
                    )
            ])

Nothing has changed so far, we have just moved the form to our own subclass from Form.

We now add the event handling method to the form. Since the button is instanciated with the value "submit"
of its attribute "event_name", epfl expects a method "handle_submit" to call for event handling (event handler methods are always prefixed with 'handle'). We provide this
method in our NoteForm class:

.. code-block:: python

	class NoteForm(components.Form):

	    ...

	    def handle_submit(self):
                if not self.validate():
                    self.page.show_fading_message(
                        'An error occurred in validating the form!', 'error'
                    )
                    return

	    print self.get_values()


What happens in handle_submit()? First, the form is validated. If validation fails (both input fields are mandatory, so validation fails
if a field is empty), an error message is displayed on the page. If validation succeeds, the form values are printed on the server console.

Next, we need to do something with the actual data that comes from the form. Enter ModelBase.
All classes inheriting from ModelBase serve as a kind of interface between the data layer (e.g. database connectors etc), and the view
(i.e. the epfl components). Since we don't want to use a full-blown database in this tutorial, we will use the ModelBase to simple implement
an in-memory storage of our notes data.

We first create our class NoteModel that will serve for storing, loading and removing notes, and insert the class to our page so it is accessible later:

.. code-block:: python

	class NoteModel(ModelBase):
	    pass

        @EPFLView(route_name='FirstStep', route_pattern='/')
        class FirstStepPage(epfl.Page):

            root_node = FirstStepRoot()
            model = NoteModel


In order to have all data management methods at hand that are needed in this tutorial, we implement the complete functionality of the NoteModel straight away.

.. code-block:: python

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


The NoteModel class stores notes as dict objects in an in-memory list and provides methods for adding, removing, getting and updating a notes,
as well as for obtaining the complete list of notes.

Every component has access to the page it is located in by using self.page. Hence, every component has access to the NoteModel as well.
We can now call add_note() on the model in the handle_submit method of our form:

.. code-block:: python

	def handle_submit(self):
	    if not self.validate():
	        self.page.show_fading_message('An error occurred in validating the form!', 'error')
	    values = self.get_values()
	    self.page.model.add_note({'title': values['title'],
	                              'text': values['text']})

The note is now persisted in memory. Ok, but how can we display it? Let's add a component that displays all created notes in a list.

This component will use a different way to retrieve its data values: Up to now, we directly set and read component attributes to handle component data.
For example, label, name and default value of the note form fields have been set in the constructor of the corresponding TextInput and Textarea classes.
While this is perfect for small amount of data or static data structures, it is not suited for complex data access operations.
Instead, we will use the get_data attribute, which enables us to create components dynamically based on the data its parent component receives.

Lets start by adding a simple Box below after the "Edit note" box:

.. code-block:: python

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
                    default_child_cls=components.Box(title='Note'),
                    get_data='notes')
            ])


We have provided three new attributes for this Box: the cid is used to access the component later, get_data="notes" tells the component to use a method load_notes() on the model to obtain the data,
and default_child_cls is used to tell the component which child to create for rendering each tem of the list that load_notes() returned.

To see an effect of this change it is important to tell the 'notes_list' component to redraw, after some changes were made. This is triggered after adding
a new entry at the end of the handle_submit handler. Each component has a redraw() method which can be triggered there. To access
a specific component the cid comes into play: every page can access its components via attribute access of the cid - independent of its position in the component or container hierarchy. So we add this line at the end of the handle_submit method:

.. code-block:: python

    def handle_submit(self):
        ...
        self.page.notes_list.redraw()

After this change, a new box inside the "My Notes" box is displayed for every notes entry we made. But the more interesting part of this is, how to adjust the data, these boxes are using? For now, they are all just called "Note" which is probably not what you want.

So we add the data_interface dict to the box that defines the fields which are available on a data object for each child. This dict maps the data given from the model (or the handle_note method to be more precise) and maps their data keys to attributes of the component. By giving the mapping value None we just simply bypass the data key to the component attribute. In a more real world example the keys can differ so you can set another data key as mapping value.

.. code-block:: python

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
                    default_child_cls=components.Box(),
                    data_interface={
                        'id': None,
                        'text': None,
                        'title': None},
                    get_data='notes')
            ])

Another example of the data_interface is show below which makes more clear, that using None is just a convenience markup.

.. code-block:: python

    data_interface={
        'id': 'id',
        'text': 'text',
        'title': 'title'
    }

Now each box of each note will display the entered title of the note. Notice, that the hard-coded title of the Box is also removed, as it is now set via the get_data/data_interface mechanism.

But we also want to display the given text of the node, not just the title. In EPFL (nearly) everything is a component - so we add one to display the text. It should appear inside the note boxes of the notes_list, so we define the node_list parameter there. To display just some text we use the (suprise!) Text component.

.. code-block:: python

    ...
    default_child_cls=components.Box(
        node_list=[
            components.Text(value='note text')
        ]
    ...

For the moment, like the box title first, every note will have the static text "note text". To inject the text of the stored note, we must access somehow the text attribute of the parent notes box, as this component has it set (via the data_interface/get_data mechanism).

To do so, there is a special attribute 'reflect'. With it, each component can access the components and container chain to traverse to the wanted data. Also, via the container_compo attribute you can access the parents container of a component. So in combination, the needed chain to access the notes text is:

.. code-block:: python

    ...
    default_child_cls=components.Box(
        node_list=[
            components.Text(value=self.reflect.container_compo.text)
        ]
    ...

If you try the code now, you will see that every creation of a new note leads to a corresponding block in the "My notes" box displaying the component information!

What's next? We can easily create another component that serves as a left-hand menu which also displays the created notes. We extend the node_list of our root component:

.. code-block:: python

    class FirstStepRoot(NoteLayout):
        def init_struct(self):
            self.node_list.extend([
                ...
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

As with the notes_list, we need to redraw the notes_link_list after adding an entry. So call redraw with the notes_link_list cid at the end of the handle_submit handler.

.. code-block:: python

    def handle_submit(self):
        ...
        self.page.notes_list.redraw()
        self.page.notes_link_list.redraw()


We used the predefined LinkListLayout component that renders its children as links.
For displaying the data, we bind the component again to notes with get_data, and set the predefined text attribute of the link to the title attribute of the note data struct.

The list also expects an URL attribute. Here, we construct the target url with the ID of the note as parameter, which we can access with {id} inside the string. If there is a corrosonding route with a view, this would work just fine. But we do not want the overhead to create a new page for it. So we declare the event_name attribute that overloads the click to a custom event handler which is defined like this:

.. code-block:: python

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

The first line queries the component, which was triggered by the click. This is done by access the first element of the epfl_event_trace attribute. This one is always available in every event handler.

Each component has a cid - even if they are not set explicit. To work with dynamically created cids you can work with the dict-like attribute 'components'. After the calling component object is available, the id of the note can be get. Now we have all informations to display a ModalBox with the detail informations of the note entry (which is, to be honest, just the same as we display in the notes_list, but the journey is the reward).

There is another interesting method called in this handler: add_component(). This method takes a component and adds it to the current container. As always after changing the container structure, a redraw is required.

Until now, we can add and display notes. But next, we want to use the note form not only for creating new notes, but also for editing existing notes.

First, how do we want to edit notes? Well, lets just provide an edit button in our list of notes. But as we also want a delete button later on, we add it, too. To make it look a bit nicer, we put them in a ColLayout instance, which results in a bootsrap-based grid row with the two cols.

.. code-block:: python

    def __init__struct(self):
        self.node_list.extend([
            ...
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
            ...

Now, we have to fill the "Edit note" form with note data once the edit button is clicked.
We first add a load_note() method on our form which fills the form with the data of an existing note:

.. code-block:: python

	class NoteForm(components.Form):

	    ...
            id = None
            compo_state = components.Form.compo_state + ["id"]

	    def load_note(self, note_id):
                note = self.page.model.get_note(note_id)
                self.id = note['id']
	        self.set_value('title', note['title'])
	        self.set_value('text', note['text'])
	        self.redraw()

Note that we have to call self.redraw(), otherwise the UI would not get updated when the form receives new data.

We also added an 'id' attribute, so the form knows which entry is edited. This attribute has to be persisted in the server-side state of EPFL. Otherwise, a page refresh
would yield in the form title and text values being restored, but the id of the form's current note would not be available anymore.
We do this by adding "id" to the compo_state list, a list that is provided by the base component where all fields are stored which are persisted
in the EPFL transaction.

Now, we simply have to call the form's load_note() method inside the handler of the edit button in our FirstStepRoot class.

.. code-block:: python

    def handle_edit_note(self):
        """ Gets triggered via the "Edit this note" Button. To read the corrosponding note, the
        event_trace is used to identify the calling component. With this information, the
        component hierarchy is used to get the needed note_id. """
        calling_cid = self.epfl_event_trace[0]
        note_id = self.page.components[calling_cid].container_compo.container_compo.id
        self.page.note_form.load_note(note_id)


Let's fix an annoying glitch: Every time we click on "Submit" in the form, a new note is created.
Our app does not know if a component already exists.

To fix this, we already added an attribute "id" for our form which stores the id of the currently displayed note.
If it is None, a new note is created if submit is clicked and the form contents are valid, otherwise, an existing note is updated.
And since we are there, we implement a method clean_form() which empties the form (which we also want to call upon submit()):

.. code-block:: python

    class NoteForm(components.Form):

        ...

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

Here, we did the following:

We set the id attribute when loading a note in the load_note() method, and we query the id attribute upon submit to decide whether a new note
has to be created or an existing one has to be updated.

The clean_form() method cleans the form and is called upon handle_submit() completes.

Finally, there is also a handle_cancel method added which could be used for a cancel button. It is on your own to add the corrosponding Button component to the form.

As a last step, we want to delete existing notes. We already added the button to the notes_list but need to implement the handler for it:

.. code-block:: python

    def handle_delete_note(self):
        """ Gets triggered via the "Delete this note" Button. To read the corrosponding note, the
        event_trace is used to identify the calling component. With this information, the
        component hierarchy is used to get the needed note_id. """
        calling_cid = self.epfl_event_trace[0]
        note_id = self.page.components[calling_cid].container_compo.container_compo.id

        if self.page.note_form.id == note_id:
            self.page.note_form.clean_form()

        self.page.model.remove_note(note_id)

That's it! We have implemented functionality to create, display, edit, and delete notes.

The first part of the tutorial is completed. You can have a look of the complete file at https://github.com/solute/pyramid_epfl/blob/master/solute/epfl/scaffolds/epfl_tutorial_scaffold/epfl_tutorial/views/first_step.py

In the second part, we extend our notes model with notes that can contain other notes, and extend the noes list by a tree that displays nested forms.
