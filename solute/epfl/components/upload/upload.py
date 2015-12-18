import base64
import requests
import ujson as json

from solute.epfl.components.form.inputbase import FormInputBase


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
    js_parts = []

    css_name = FormInputBase.css_name + [("solute.epfl.components:upload/static", "upload.css"), ]

    template_name = "upload/upload.html"

    compo_state = FormInputBase.compo_state + ["allowed_file_types", "show_remove_icon", "maximum_file_size",
                                               "handle_click", "store_async", "height", "width", "file_infos",
                                               "maximum_image_width",  "maximum_image_height", "minimum_image_width",
                                               "minimum_image_height","use_old_value_format"]

    height = None  #: Compo height in px if none nothing is set

    width = None  #: Compo width in px if none nothing is set

    plus_icon_size = "5x"  #: The plus icon in dropzone, use the font awesome sizes 1x - 5x or lg

    #: Set true to hide the preview image for the uploaded file.
    no_preview = False

    #: Set to true to show the file name instead of the input field if value is set
    file_upload_input_preview = True

    #: The type of validator that will be used for this field.
    validation_type = 'text'

    #: Sends changes immediately
    fire_change_immediately = True

    #: Allowed file types if not allowed nothing happens: give a list with file type endings example: ["png","gif","jpg"]
    allowed_file_types = None

    #: show a remove icon which removes the current uploaded file see: handle_remove_icon
    show_remove_icon = True

    #: maximum file size in byte this is checked in javascript,
    #: the hard technical browser limit is 100 MB so if a file bigger than 100 mb is dropped the browser crashes
    maximum_file_size = 5 * 1024 * 1024

    #: maximum width ( resolution ) of an uploaded image if the file is no image this check does nothing
    maximum_image_width = None

    #: maximum height ( resolution ) of an uploaded image if the file is no image this check does nothing
    maximum_image_height = None

    #: minimum width ( resolution ) of an uploaded image if the file is no image this check does nothing
    minimum_image_width = None

    #: minimum height ( resolution ) of an uploaded image if the file is no image this check does nothing
    minimum_image_height = None

    #: Shows the file input
    show_file_upload_input = True

    #: shows the dropzone
    show_drop_zone = False

    #: Margin of drop zone icon and label in percentage from the upper drop zone border.
    #: Can be adapted in order to yield reasonable layout based on different drop zone icon sizes
    drop_zone_add_position_top = 35

    #: Additional label text shown in the drop zone, if set
    drop_zone_add_text = None

    #: Generate a handle_click event if the component is clicked on by the user.
    handle_click = False

    #: Upload the image immediately via handle_store, store has to return a URI that will be used as value.
    store_async = False

    file_infos = None  #: infos about the uploaded files

    #: This is required for backward compatibilty in older versions only the base64 string or url was in data in new
    #: version its always a list
    use_old_value_format = True

    #: This error is shown via javascript if image size is not correct
    error_message_image_size_to_big = "Image Size is too big "
    #: This error is shown via javascript if image size is not correct
    error_message_image_size_to_small = "Image Size is too small"
    #: This error is shown via javascript if file size is not correct
    error_message_file_size = "File size to big"
    #: This error is shown via javascript if file type is not allowed
    error_message_file_type = "This File Type is not allowed"

    new_style_compo = True
    compo_js_params = FormInputBase.compo_js_params + ['allowed_file_types', 'show_remove_icon', 'maximum_file_size',
                       'value', 'handle_click', 'store_async', 'show_file_upload_input', 'show_drop_zone',
                       "maximum_image_width", "maximum_image_height", "error_message_image_size_to_big","error_message_image_size_to_small",
                       "error_message_file_size", "error_message_file_type","minimum_image_width", "minimum_image_height",]
    compo_js_extras = ['handle_drop', 'handle_click']
    compo_js_name = 'Upload'

    def __init__(self, page, cid,
                 label=None,
                 name=None,
                 default=None,
                 validation_type=None,
                 handle_click=None,
                 store_async=None,
                 height=None,
                 width=None,
                 plus_icon_size=None,
                 no_preview=None,
                 file_upload_input_preview=None,
                 fire_change_immediately=None,
                 allowed_file_types=None,
                 show_remove_icon=None,
                 maximum_file_size=None,
                 maximum_image_width=None,
                 maximum_image_height=None,
                 minimum_image_width=None,
                 minimum_image_height=None,
                 show_file_upload_input=None,
                 show_drop_zone=None,
                 drop_zone_add_position_top=None,
                 drop_zone_add_text=None,
                 use_old_value_format=None,
                 error_message_image_size_to_big=None,
                 error_message_image_size_to_small=None,
                 error_message_file_size=None,
                 error_message_file_type=None,
                 **extra_params):
        """Download component.

        :param label: Optional label describing the input field.
        :param name: An element without a name cannot have a value.
        :param default: Default value that may be pre-set or pre-selected
        :param validation_type: The type of validator that will be used for this field
        :param handle_click: Generate a handle_click event if the component is clicked on by the user.
        :param store_async: Upload the image immediately via handle_store, store has to return a URI that will be used
                            as value.
        :param height: Compo height in px if none nothing is set
        :param width: Compo width in px if none nothing is set
        :param plus_icon_size: The plus icon in dropzone, use the font awesome sizes 1x - 5x or lg
        :param no_preview: Set true to hide the preview image for the uploaded file.
        :param file_upload_input_preview: Set to true to show the file name instead of the input field if value is set
        :param fire_change_immediately: Sends changes immediately
        :param allowed_file_types: Allowed file types if not allowed nothing happens: give a list with file type
                                   endings example: ["png","gif","jpg"]
        :param show_remove_icon: show a remove icon which removes the current uploaded file see: handle_remove_icon
        :param maximum_file_size: maximum file size in byte this is checked in javascript,
                                  the hard technical browser limit is 100 MB so if a file bigger than 100 mb is dropped
                                  the browser crashes
        :param maximum_image_width: maximum width ( resolution ) of an uploaded image if the file is no image this check
                                    does nothing
        :param maximum_image_height: maximum height ( resolution ) of an uploaded image if the file is no image this
                                     check does nothing
        :param minimum_image_width: minimum width ( resolution ) of an uploaded image if the file is no image this
                                    check does nothing
        :param minimum_image_height: minimum height ( resolution ) of an uploaded image if the file is no image this
                                     check does nothing
        :param show_file_upload_input: shows the file input
        :param show_drop_zone: shows the dropzone
        :param drop_zone_add_position_top:  Margin of drop zone icon and label in percentage from the upper drop zone
                                            border. Can be adapted in order to yield reasonable layout based on
                                            different drop zone icon sizes
        :param drop_zone_add_text: Additional label text shown in the drop zone, if set
        :param use_old_value_format: This is required for backward compatibilty in older versions only the base64 string
                                     or url was in data in new version its always a list
        :param error_message_image_size_to_big: This error is shown via javascript if image size is not correct
        :param error_message_image_size_to_small: This error is shown via javascript if image size is not correct
        :param error_message_file_size: This error is shown via javascript if file size is not correct
        :param error_message_file_type: This error is shown via javascript if file type is not allowed
        """
        super(Upload, self).__init__(page, cid,
                                     label=label,
                                     name=name,
                                     default=default,
                                     validation_type=validation_type,
                                     handle_click=handle_click,
                                     store_async=store_async,
                                     height=height,
                                     width=width,
                                     plus_icon_size=plus_icon_size,
                                     no_preview=no_preview,
                                     file_upload_input_preview=file_upload_input_preview,
                                     fire_change_immediately=fire_change_immediately,
                                     allowed_file_types=allowed_file_types,
                                     show_remove_icon=show_remove_icon,
                                     maximum_file_size=maximum_file_size,
                                     maximum_image_width=maximum_image_width,
                                     maximum_image_height=maximum_image_height,
                                     minimum_image_width=minimum_image_width,
                                     minimum_image_height=minimum_image_height,
                                     show_file_upload_input=show_file_upload_input,
                                     show_drop_zone=show_drop_zone,
                                     drop_zone_add_position_top=drop_zone_add_position_top,
                                     drop_zone_add_text=drop_zone_add_text,
                                     use_old_value_format=use_old_value_format,
                                     error_message_image_size_to_big=error_message_image_size_to_big,
                                     error_message_image_size_to_small=error_message_image_size_to_small,
                                     error_message_file_size=error_message_file_size,
                                     error_message_file_type=error_message_file_type,
                                     **extra_params)

    def handle_change(self, value):
        """
        When an image gets dropped over the dropzone or an image is choosen in file input
        :param value: a list in format [{"name":filename or url, "data":base64 string or url"}...]
        """

        # This check is needed for backward compatibility in older versions only the base64 string or url was in data

        if self.use_old_value_format:
            if value and len(value) == 1:
                self.value = value[0]["data"]
            else:
                self.value = value
        else:
            self.value = value

        if self.no_preview is False:
            self.redraw()

    def handle_store(self, files):
        self.add_ajax_response(json.encode(self.store(files)))

    def store(self, files):
        """
        :param files: list of dicts in the format [{'name': 'ABC': 'data': <url or base_64 encoded file>}, ... ]
        :return A list in the format [{'name': 'ABC': 'data': <any return value, e.g. an uploaded URL>,
                                       'xy': <arbirtrary additional values are possible>}, ... ]
        """
        return files

    def _extract_binary(self,value):
        """extracts binary data from base64 string or url
        :param value: base64 string from browser or url
        :return: binary data
        """
        binary = None
        if str(value).startswith('http') is True:
            # Upload data is from another url, so we have to parse it first
            binary = requests.get(value).content
        else:
            info, coded_string = str.split(str(value), ',')
            binary = base64.b64decode(coded_string)

        return binary

    def get_as_binary(self):
        """
        :return: self.value as binary if self.value is a list then a list of binary and meta infos will be returned
        """
        value = self.value
        if value is None:
            return value

        if type(value) == list:
            result = []
            for val in self.value:
                result.append({"name":val["name"],"data":val["data"],"binary":self._extract_binary(val["data"])})
            return result
        else:
            return self._extract_binary(value)

    def handle_remove_icon(self):
        self.value = None
        self.redraw()

    def handle_drop_accepts(self, cid, moved_cid):
        self.add_ajax_response('true')


    def handle_file_info(self,file_infos):
        """
        Called before the actual upload to set file information
        @param file_infos: list of dicts. Each dicts holds information for one selected file
        """
        self.file_infos = file_infos
