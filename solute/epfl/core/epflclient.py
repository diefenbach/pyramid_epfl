# coding: utf-8
"""

This module contains a javascript-wrapper, which composes JS-Strings to communicate with the epfl.js-client-library
Extra-Content-Handling is here!

"""

import jinja2
import string
import ujson as json


def quote_escape_html(html):
    html = html.replace("\"", "\\\"")
    return '"%s"' % html


def quote_escape_js(js):
    return json.encode(js)


def replace_html(id, html):
    return "$('#%s').html(%s)" % (id, quote_escape_html(html))


def make_js_call(call, *args):
    """ returns a js-snipped calling a method with the given parameters.
    The parameters are escaped and quoted as necessary """

    js = [call]

    js.append("(")
    first = True
    for arg in args:
        if first:
            first = False
        else:
            js.append(",")
        js.append(json.encode(arg))
    js.append(")")

    return string.join(js, "")


class ExtraContent(object):

    enclose = None
    target = None # http-header, head, footer
    exclusive = False

    # Dynamic Components need to be able to push content dynamically.
    enable_dynamic_rendering = False

    def __new__(cls, data):
        """ Nifty little trick: if you create an Extra-Content with a list of Extra-Content, you get a list of Extra-Content-Objects """
        if type(data) is list:
            return [cls(el) for el in data]
        else:
            return super(ExtraContent, cls).__new__(cls)

    def __init__(self, data):
        self.data = data

    def get_content_id(self):
        """ Über diese ID wird gestuert, ob mehrfach-hinzufügen von Head-Content für diese Seite erlaubt ist oder nicht.
        Es wird nur Head-Content eingefügt, welcher entweder hier None liefert, oder noch kein anderer head-content vorhanden ist,
        welcher diese content_id liefert.
        zum überschreiben
        """
        return None # Default-Mässig alle Contents akzeptieren

    def render(self):
        return self.data


class CSSContent(ExtraContent):
    """ Instances of this class can be passed to the function "wtf.response.add_jinja_extra_content".
    It will normally rendered in the template at the top of the page using {{ css_imports() }}.
    Links to external CSS-Files go here.
    """
    target = "head"


class JSContent(ExtraContent):
    """ Instances of this class can be passed to the function "wtf.response.add_jinja_extra_content".
    It will normally rendered in the template at the bottom of the page using {{ js_imports() }}.
    Links to external JS-Files go here.
    """
    target = "footer"


class JSBlockContent(ExtraContent):
    """ Instances of this class can be passed to the function "wtf.response.add_jinja_extra_content".
    It will normally rendered in the template at the bottom of the page using {{ js_imports() }}. All
    extra-content added to the response will be sourrounded by a ondocument-ready-function.
    JS-Snippets go here.
    """
    enclose = "<script>$(document).ready(function(){", "});</script>"
    target = "footer"

    def render(self):
        data = self.data.strip()
        if data.startswith("<script"):
            data = data[data.index(">") + 1:]
        if data.endswith("</script>"):
            data = data[:-9]
        return data


class JSLink(JSContent):
    """ A class managing the javascript-imports (via script-tags).
    It returns it´s src-path as unique-id, so even if requested multiple times, the script-tag will only
    be once rendered.
    """
    target = "footer"
    enable_dynamic_rendering = True

    def get_content_id(self):
        return self.data # src-path as unique-id

    def render(self):
        """ we are a script-tag! """
        return "<script src='%s' language='javascript'></script>\r\n" % self.data


class CSSLink(CSSContent):
    """ Same story as JSLink but for CSS """

    target = "head"
    enable_dynamic_rendering = True

    def get_content_id(self):
        return self.data # src-path as unique-id

    def render(self):
        """ we are a css-link """
        return '<link rel="stylesheet" type="text/css" href="%s"/>\r\n'  % self.data


class EPFLResponse(object):

    """ Collects side-effect responses.
    It is always bound to a single page and therefore only contains the output of a single page.
    The self.render_ajax_response, self.get_exclusive_extra_content and self.render_extra_content-functions

    """
    _ajax_response = None

    def __init__(self, page_obj):
        self.page_obj = page_obj
        self.page_request = page_obj.page_request
        self.request = page_obj.request
        self.ajax_response = []
        self.extra_content = []
        self.content_type = "text/html; charset=utf-8"

    @property
    def ajax_response(self):
        if type(self._ajax_response) is not list:
            return self._ajax_response
        out = []
        for v in self._ajax_response:
            if type(v) is not tuple:
                v = (0, v)
            out.append(v)
        out.sort(key=lambda x: x[0])
        self._ajax_response = out
        return [v for k, v in self._ajax_response]

    @ajax_response.setter
    def ajax_response(self, value):
        self._ajax_response = value

    def add_ajax_response(self, resp_string):
        """
        Adds a js string to the response for ajax-requests. Accepts string or (execution_order, string) tuples.
        """
        if type(self._ajax_response) is list:
            self._ajax_response.append(resp_string)

    def answer_json_request(self, resp_obj):
        """ The response consists only of this object which will be json-encoded - in case it's an answer to a epfl.json_request.
        The object is available at the client's callback-function.
        """
        self.content_type = "application/json; charset=utf-8"
        self.ajax_response = json.encode(resp_obj)

    def render_ajax_response(self):
        """ Has to be called from the view-controller if we have an ajax-request (checked by self.handle_ajax_request).
        This returns the contents added by the components with "response.add_ajax_response" or "response.answer_json_request".
        """

        out = []

        if type(self.ajax_response) is not list:
            self.ajax_response = [self.ajax_response]

        for el in self.ajax_response:
            if type(el) is unicode:
                out.append(el)
            else:
                try:
                    # First try pythons standards, an asci encoded string will be decoded and a unicode will be
                    # returned.
                    out.append(unicode(el))
                except UnicodeDecodeError:
                    # In case of error we support utf-8, nothing else.
                    out.append(unicode(el.decode('utf-8')))

        # collect the other-pages js
        for page_obj in self.page_request.get_handeled_pages():
            other_js = page_obj.response.render_ajax_response()
            if other_js:
                out.append('epfl.exec_in_page("{tid}", {other_js})'.format(tid = page_obj.transaction.get_id(),
                                                                           other_js = quote_escape_js(other_js)))

        return string.join(out, "")

    def add_extra_content(self, extra_content):
        if type(extra_content) is list:
            self.extra_content.extend(extra_content)
        else:
            self.extra_content.append(extra_content)

    def get_exclusive_extra_content(self):
        for extra_content in self.extra_content:
            if extra_content.exclusive:
                return extra_content.render()
        return None

    def render_jinja(self, template, **kwargs):
        if type(template) is str:
            env = self.request.get_epfl_jinja2_environment()
            tpl = env.get_template(template)
        else:
            tpl = template
        return tpl.render(**kwargs)

    def render_extra_content(self, target):

        out = []
        enclosed_out = {}
        content_ids = set()
        for extra_content in self.extra_content:
            if extra_content.target != target:
                continue

            if extra_content.enclose:
                eout = enclosed_out.setdefault(extra_content.enclose, [])
                eout.append(extra_content.render())
                enclosed_out[extra_content.enclose] = eout
            else:
                content_id = extra_content.get_content_id()
                if content_id not in content_ids:
                    out.append(extra_content.render())
                    if content_id is not None:
                        content_ids.add(content_id)

        for enclose, eout in enclosed_out.items():
            out.append(enclose[0])
            out.extend(eout)
            out.append(enclose[1])

        return jinja2.Markup(string.join(out, ""))

