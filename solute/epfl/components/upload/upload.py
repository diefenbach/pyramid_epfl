import base64
import requests

from solute.epfl.components.form.form import FormInputBase


class Upload(FormInputBase):
    """
    A form upload field.
    
    Typically, this component is used in a form:
    
    .. code:: python
        
        form = Form(node_list=[Upload(label="Image:", name="image")])
    
    """

    js_name = FormInputBase.js_name + [("solute.epfl.components:upload/static", "upload.js"),
                                       ("solute.epfl.components:upload/static", "jquery.iframe-transport.js"),
                                       ("solute.epfl.components:upload/static", "jquery.fileupload.js")]

    css_name = FormInputBase.css_name + [("solute.epfl.components:upload/static", "upload.css"), ]

    template_name = "upload/upload.html"

    compo_state = FormInputBase.compo_state + ["allowed_file_types", "show_remove_icon", "maximum_file_size", "type",
                                               "dropped_cid"]

    #: Set true to hide the preview image for the uploaded file.
    no_preview = False

    #: The type of validator that will be used for this field.
    validation_type = 'text'

    #: Sends changes immediately
    fire_change_immediately = True

    #: Allowed file types if not allowed nothing happens: give a list with file type endings example: ["png","gif","jpg"]
    allowed_file_types = None

    #: show a remove icon which removes the current uploaded file see: handle_remove_icon
    show_remove_icon = False

    #: maximum file size in byte this is checked in javascript, the hard limit is 200 MB
    maximum_file_size = 5 * 1024 * 1024

    #: Shows the file input
    show_file_upload_input = True

    #: shows the dropzone
    show_drop_zone = False

    #: height of dropzone
    drop_zone_height = 250

    #: image type / source
    type = None

    #: cid of the dropped image
    dropped_cid = None

    #: Source of the image is desktop
    TYPE_DESKTOP = "desktop"

    #: Source of the image is a image that is no epfl compo
    TYPE_EXTERN = "extern"

    #: source of the image is epfl upload compo
    TYPE_EPFL_UPLOAD_IMAGE = "epfl-upload-image"

    #: source of the image is epfl image compo
    TYPE_EPFL_IMAGE = "epfl-img-component-image"

    new_style_compo = True
    compo_js_params = ['fire_change_immediately', 'allowed_file_types', 'show_remove_icon', 'maximum_file_size',
                       'value']
    compo_js_name = 'Upload'
    compo_js_extras = ['handle_click']

    def __init__(self, page, cid, label=None, name=None, default="", validation_type="", **extra_params):
        """Download component.

        :param label: Optional label describing the input field.
        :param name: An element without a name cannot have a value.
        :param default: Default value that may be pre-set or pre-selected
        :param validation_type: The type of validator that will be used for this field
        """
        super(Upload, self).__init__(page, cid, label, name, default, validation_type)

    def handle_change(self, value, type=None, dropped_cid=None):
        """
        When an image gets dropped over the dropzone or an image is choosen in file input
        :param url: image url if the image's source is desktop or epfl image compo url is a byte string
        :param type: one of the TYPE constants
        :param dropped_cid: if the dropped image is an epfl compo this is the cid
        """
        self.value = value
        self.type = type
        self.dropped_cid = dropped_cid
        if self.no_preview is False:
            self.redraw()

    def handle_click(self):
        """
        click on Dropzone
        """
        pass

    def get_as_binary(self):
        value = self.value
        if str(value).startswith('http') is True:
            # Upload data is from another url, so we have to parse it first
            binary = requests.get(value).content
        else:
            info, coded_string = str.split(str(value), ',')
            binary = base64.b64decode(coded_string)
        return binary

    def handle_remove_icon(self):
        self.value = None
        self.redraw()
