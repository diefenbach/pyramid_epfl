from solute.epfl.core import epflcomponentbase


class Form(epflcomponentbase.ComponentContainerBase):

    # core internals
    template_name = "form/form.html"
    asset_spec = "solute.epfl.components:form/static"
    js_name = ["form.js"]
    compo_state = ["_registered_fields", "is_dirty"]

    # js settings
    compo_js_auto_parts = True
    compo_js_name = 'Form'
    compo_js_params = ['event_name']

    # custom compo attributes
    _registered_fields = None  #: Private cache of the fields registered with this form.
    is_dirty = False  #: Flag whether the form has had any change of value since initialisatio
    event_name = 'submit'  #: Default name of the event handling method (without trailing "handle\_").

    # internal compo attributes
    validate_hidden_fields = False  #: Flag to determine whether hidden fields will be validated. TODO: DEFECTIVE!

    def __init__(self, page, cid,
                 node_list=None,
                 validate_hidden_fields=None,
                 event_name=None,
                 **extra_params):
        """Generates a form container with some convenience handling for child components with name and value.

        :param node_list: List of child components.
        :param validate_hidden_fields: Flag to determine whether hidden fields will be validated.
        :param event_name: Default name of the event handling method (without trailing "handle\_").
        """
        pass

    def handle_submit(self):
        pass

    def handle_set_dirty(self):
        self.is_dirty = True

    def get_parent_form(self):
        return self

    def register_field(self, field):
        """
        Make a field known to the parent form. Since any component can reside in a form, the child components
        which register themselves as fields have to provide the methods reset() and validate()
        (see :class:`.FormInputBase`), since these are called for all registered fields by the parent form.
        """
        if self._registered_fields is None:
            self._registered_fields = set()
        self._registered_fields.add(field.cid)

    def unregister_field(self, field):
        try:
            self._registered_fields.remove(field.cid)
        except (AttributeError, KeyError):
            pass

    @property
    def registered_fields(self):
        if self._registered_fields is None:
            self._registered_fields = set()
        return [self.page.components[cid] for cid in self._registered_fields]

    @property
    def registered_names(self):
        if self._registered_fields is None:
            self._registered_fields = set()
        return dict([
            (self.page.components[cid].name, self.page.components[cid]) for cid in self._registered_fields
            if hasattr(self.page.components[cid], 'name') and self.page.components[cid].name is not None])

    def set_value(self, key, value):
        for field in self.registered_fields:
            if field.name == key:
                field.value = value
                return

    def reset(self):
        """
        Initialize all registered form fields with its default value and clear all validation messages.
        """
        for field in self.registered_fields:
            field.set_to_default()
        self.redraw()
