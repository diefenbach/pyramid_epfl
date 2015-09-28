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

    js_name = [("solute.epfl.components:download/static", "download.js"),
               ("solute.epfl.components:download/static", "FileSaver.min.js")]
    compo_js_name = 'Download'

    def __init__(self, page, cid, label=None, value=None, event_name=None, event_target=None, is_submit=False,
                 **extra_params):
        """Download component.

        :param label: If set, the label is rendered before the button.
        :param value: The value is used as button text if no icon is provided.
        :param event_name: Mandatory name of the event handling method (without trailing "handle\_").
        :param event_target: Optional target where the event handling method can be found.
        :param is_submit: Set to true if button should have html type "submit".
        """
        super(Download, self).__init__(page, cid, label, value, event_name, event_target, is_submit)
