# * encoding: utf-8

from dateutil import parser as dateutil_parser
from datetime import datetime
import pytz

from solute.epfl.components.form.inputbase import FormInputBase


class DatetimeInput(FormInputBase):

    # core internals
    template_name = "datetime_input/datetime_input.html"
    js_name = FormInputBase.js_name + [("solute.epfl.components:datetime_input/static", "datetime_input.js"),
                                       ("solute.epfl.components:datetime_input/static", "moment-with-locales.min.js"),
                                       ("solute.epfl.components:datetime_input/static",
                                        "bootstrap-datetimepicker.min.js")]
    css_name = FormInputBase.css_name + [("solute.epfl.components:datetime_input/static",
                                          "bootstrap-datetimepicker.min.css")]
    compo_state = FormInputBase.compo_state + ["date_format"]

    # js settings
    compo_js_params = FormInputBase.compo_js_params + ['date_format', "value"]
    compo_js_name = 'DatetimeInput'

    # custom definitions
    DATE_FORMAT_LOCALE = "LL"  #: Constant for locale format example: 18. Juli 2015
    DATE_FORMAT_MONTH_YEAR = "MM[/]YYYY"  #: Constant for month year format example: 08/2015
    DATE_FORMAT_YEAR = "YYYY"  #: Constant for year format example: 2015
    DATE_FORMAT_LOCALE_WITH_TIME = "LLL"  #: Constant for locale format with time example: 18. Juli 2015 00:00
    DATE_FORMAT_ISO_TTMMJJJJ = "DD.MM.YYYY"  #: Constant for locale format: 31.12.2015

    # custom compo attributes
    calendar_icon = True  #: Set to true if calendar overlay icon should be displayed
    date_format = DATE_FORMAT_LOCALE_WITH_TIME  #: This is the date format from moment.js http://momentjs.com/

    def __init__(self, page, cid,
                 name=None,
                 default=None,
                 label=None,
                 mandatory=None,
                 value=None,
                 strip_value=None,
                 validation_error=None,
                 fire_change_immediately=None,
                 placeholder=None,
                 readonly=None,
                 submit_form_on_enter=None,
                 input_focus=None,
                 label_style=None,
                 input_style=None,
                 layout_vertical=None,
                 compo_col=None,
                 label_col=None,
                 date_format=None,
                 calendar_icon=None,
                 **extra_params):
        """Datetime Input using bootstrap datime picker and moment js

        :param name: An element without a name cannot have a value
        :param default: Default value that may be pre-set or pre-selected
        :param label: Optional label describing the input field
        :param mandatory: Set to true if value has to be provided for this element in order to yield a valid form
        :param value: The actual value of the input element that is posted upon form submission
        :param strip_value: strip value if True in get value
        :param validation_error: Set during call of :func:`validate` with an error message if validation fails
        :param fire_change_immediately: Set to true if input change events should be fired immediately to the server.
                                        Otherwise, change events are fired upon the next immediate epfl event
        :param placeholder: Placeholder text that can be displayed if supported by the input
        :param readonly: Set to true if input cannot be changed and is displayed in readonly mode
        :param submit_form_on_enter: If true, underlying form is submitted upon enter key in this input
        :param input_focus: Set focus on this input when component is displayed
        :param label_style: Can be used to add additional css styles for the label
        :param input_style: Can be used to add additional css styles for the input
        :param layout_vertical: Set to true if label should be displayed on top of the input and not on the left before
                                it
        :param compo_col: Set the width of the complete input component (default: max: 12)
        :param label_col: Set the width of the complete input component (default: 2)
        :param validation_type: Set the validation type, default 'text'
        :param date_format: #: This is the date format from moment.js http://momentjs.com/
        :param calendar_icon: Set to true if calendar overlay icon should be displayed
        """
        pass

    def to_utc_value(self):
        # remove timezone if date_format is in year, month or day granularity.
        # In this case, we can just drop the timezone (1 Jul 2012 GMT == 1 Jul 2012 UTC).
        # Otherwise, convert to UTC (1 Jul 2012 00:00 GMT == 30 Jun 2011 22:00 UTC)
        if self.value is None:
            return None
        datetime_object = dateutil_parser.parse(self.value)
        if self.date_format in [self.DATE_FORMAT_LOCALE, self.DATE_FORMAT_MONTH_YEAR, self.DATE_FORMAT_YEAR]:
            datetime_object = datetime_object.replace(tzinfo=None)
        else:
            datetime_object = datetime_object.astimezone(pytz.timezone("UTC"))
        return datetime.isoformat(datetime_object)
