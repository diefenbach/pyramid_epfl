import ujson as json
from solute.epfl.components import Button


class Download(Button):
    """
    This component provides basic download button functionality.

    To use a download button, a event handling method for handling the button clicks has to be provided:

    .. code:: python

        download = Download(name="Do something", event_name="submit")

        def handle_submit(self):
            file = [data, filename]
            self.return_ajax_response(file)
            # get the data that should be downloaded and return them using ajax

   """

    # core internals
    js_name = Button.js_name + [("solute.epfl.components:download/static", "download.js"),
                                ("solute.epfl.components:download/static", "FileSaver.min.js")]

    # js settings
    compo_js_name = 'Download'
    compo_js_params = Button.compo_js_params + ['download_direct']

    # custom compo attributes

    #: Download the file(s) direct.
    download_direct = False
    #: The type of the downloaded file.
    file_type = 'text/csv'

    def __init__(self, page, cid,
                 label=None,
                 value=None,
                 color=None,
                 icon=None,
                 icon_size=None,
                 icon_color=None,
                 tooltip=None,
                 event_name=None,
                 event_target=None,
                 is_submit=None,
                 confirm_first=None,
                 confirm_message=None,
                 button_size=None,
                 disable_on_click=None,
                 stop_propagation_on_click=None,
                 download_direct=None,
                 **extra_params):
        """Download component.

        :param label: If set, the label is rendered before the button
        :param value: The value is used as button text if no icon is provided
        :param color: Optional color of the button. Possible values: default, primary, warning, danger, success,
                      transparent
        :param icon: Optional font-awesome icon to be rendered as button value instead of the text attribute
        :param icon_size: Optional font-awesome icon-size possible values: 'lg', 2, 3, 4, 5
        :param icon_color: Optional color of the button icon. Possible values default, primary, warning, danger, success
        :param tooltip: Optional tooltip text that is placed on the button
        :param event_name: Mandatory name of the event handling method (without trailing "handle\_")
        :param event_target: Optional target where the event handling method can be found
        :param is_submit: Set to true if button should have html type "submit"
        :param disabled: Set to true if button should be disabled
        :param confirm_first: Set to true if user should be asked for confirmation first before the button event is
                              triggered
        :param confirm_message: Adapt this text for a custom confirmation dialog message
        :param button_size: Optional button size. Possible values: 'btn-lg', 'btn-sm', 'btn-xs'
        :param disable_on_click: If set to true, the html button (not the component!) is set to disabled on a click
        :param stop_propagation_on_click: Set to true if click event should not be propagated to parent components
        :param download_direct: Download the file(s) direct
        """
        if not self.event_target:
            self.event_target = self.cid

    def handle_direct_download(self, cid):
        """
        Calls the internal direct_download-function which must return the download data and the filename.
        Will add a js response which calls to the js-function do_download with given data, (file-)type and filename.

        Params:
            cid (str): The cid of the event-target-component
        """
        data, filename = self.direct_download()
        if not data:
            return
        download_data = json.encode({'data': data, 'type': self.file_type, 'name': filename})
        self.add_js_response('epfl.components["%s"].do_download(%s)' % (cid, download_data))

    def direct_download(self):
        """ Default direct_download function

        This is the default direct_download function which just returns the download-components value (which typically
        is its button text and the string 'default.csv' as filename.
        This should be overwritten and perform the actions needed for downloading.
        If you want to stop the download process (e.g. because some validation failed or the download data is not there
        yet) you should return False and an arbitrary second parameter (False is recommended)
        """
        return self.value, 'default.csv'

    def handle_after_download(self):
        """
        Overwrite this function to implement actions that should happen after downloading (like closing a modal-box...)
        This function will be called from inside of the js-function do_download.
        """
        pass
