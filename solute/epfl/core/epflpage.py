# coding: utf-8

import pyramid
import epflcomponentbase, epfltransaction, epflclient
import types
import string

from odict import odict

from pyramid.httpexceptions import HTTPUnauthorized
from pyramid import security

from solute.epfl import json
from solute.epfl.jinja import jinja_helpers

from solute.epfl.core import epflclient, epflutil

def dummy_decorator(func):
    return func

class Page(object):

    """
    Container for the components of the page.

    The parameter "name" must be unique for the complete application!

    There are three response-modes:
    - full-page: a complete html-page (including <script>-tags) are returned and rendered by the browser.
                 This is normally requested by a link (GET) or a submit (POST)

    - event-queue-response: multiple js-snippets are returned and evaluted at client side.
                            This is requested by a epfl.send(...) request from the client side.

    - ajax-json-response: a single json-string returned to an manually created ajax-request.
                          (eventually generated by a js-library, called on the client by epfl.ajax_request(...) )
    """

    __acl__ = [(security.Allow, security.Everyone, 'access')]

    asset_spec = "solute.epfl:static"

    js_name = ["js/jquery-1.8.2.min.js",
               "js/jquery-ui.js",
               "js/epfl.js",
               "js/epflcomponentbase.js",
               "js/json2-min.js"]

    css_name = ["css/epfl.css",
                "css/jquery-ui-lightness/jquery-ui-1.8.23.custom.css",
               "css/font-awesome/css/font-awesome.min.css" ]


    template = "page.html" # the name of the template used to render this page
    base_html = 'base.html'

    root_cls = None
    title = 'Empty Page'

    overlay_title = "Overlay" # If this page is displayed as overlay, use this title.

    overlay_options = None # Mandatory, if this page is displayed as overlay.
                           # Use these options:
                           # {"resizeable": True,
                           #  "modal": True,
                           #  "draggable": True,
                           #  "height": 400,
                           #  "width": 600,
                           #  "position": "center"}

    __name = None # cached value from get_name()

    def __init__(self, request, transaction = None):
        """ The optional parameter "transaction" is needed when creating page_objs manually.
        So the transaction is not the same as the requests one.
        """

        self.request = request
        self.page_request = PageRequest(request, self)
        self.response = epflclient.EPFLResponse(self)

        self.__parent = None

        self.data = {"css_imports": self.get_css_imports,
                     "js_imports": self.get_js_imports}  # additional variables for page
                                                         # use it, by assigning directly to this dictionary:
                                                         # e.g.
                                                         # page.data["something"] = some_object

        self.components = odict() # all registered components of this page
        env = request.get_epfl_jinja2_environment()
        self.jinja_template = env.get_template(self.template)
        env.globals['epfl_base_html'] = self.base_html
        env.globals['epfl_base_title'] = self.title

        self.jinja_template.module # this access triggers the parsing of the template
                                   # this is neccessary because this parsing
                                   # collects additional meta-data from the template via
                                   # the epfl-jinja-component-extension (jinja_extensions.py)

##        request.register_template_usage(self.template, self) # tells the request which page is in use



        if transaction:
            self.transaction = transaction
        else:
            self.transaction = self.__get_transaction_from_request()


    def __call__(self):
        """
        MAIN-ENTRY-POINT

        The method that gets called from the outside framework to diplay this page.
        This is the main-handler for the (framework's) request.
        The output of other handeled pages (overlays) are allready collected in place (epflclient.EPFLResponse)
        [request-processing-flow]
        """

        if not self.has_access():
            raise HTTPUnauthorized()

        # handling the "main"-page...
        self.create_components()

        try:
            if self.handle_ajax_request():
                out = self.response.render_ajax_response()
                extra_content = [s.render() for s in self.response.extra_content if s.enable_dynamic_rendering]
                extra_content = [s for s in extra_content if s not in self.transaction['rendered_extra_content']]
                out = "epfl.handle_dynamic_extra_content(%s);\r\n%s" % (json.dumps(extra_content), out)
                self.transaction['rendered_extra_content'].update(extra_content)
            else:
                self.handle_submit_request()
                out = self.render()
                extra_content = set([s.render() for s in self.response.extra_content if s.enable_dynamic_rendering])
                self.transaction['rendered_extra_content'] = self.transaction.get('rendered_extra_content', set())
                self.transaction['rendered_extra_content'].update(extra_content)

        finally:
            self.done_request()

            self.request.session.save() # performance issue! should only be called, when session is modified!
            self.request.session.persist() # performance issue! should only be called, when session is modified!


        return pyramid.response.Response(body = out.encode("utf-8"),
                                         content_type = "text/html; charset=utf-8",
                                         status = 200) # todo

    def create_components(self):
        """ Calling self.setup_components once and remember the compos as compo_info """
        if not self.transaction.get("components_assigned"):
            self.setup_components()
            compo_info = []
            for cid, compo in self.components.items():
                compo_info.append(compo.get_component_info())
            self.transaction["compo_info"] = compo_info
            self.transaction["components_assigned"] = True
        else:
            for compo_info in self.transaction["compo_info"]:
                self.assign_component(compo_info)


    def assign_component(self, compo_info):
        """ Create a component from the remembered compo_info and assign it to the page """
        compo_obj = compo_info["class"].create_by_compo_info(self, compo_info)
        self.add_static_component(compo_info["cid"], compo_obj)


    @property
    def parent(self):
        """ Gets the parent-page (connected by the parent-transaction) - if any!
        It "spawns" a new page-obj-live-cycle with setup_component and via the PageRequest (get_handeled_pages) the
        hook for the teardown (done_request).
        """
        if self.__parent:
            return self.__parent

        ptid = self.transaction.get_pid()
        if not ptid:
            raise ValueError, "No parent page connected to this page"

        parent_transaction = epfltransaction.Transaction(self.request, ptid)
        parent_page_name = parent_transaction.get_page_name()
        parent_page_class = epflutil.get_page_class_by_name(self.request, parent_page_name)

        parent_page_obj = parent_page_class(self.request, parent_transaction)
##        parent_page_obj.setup_components()

        self.page_request.add_handeled_page(parent_page_obj)

        self.__parent = parent_page_obj

        return parent_page_obj



    def done_request(self):
        """ [request-processing-flow]
        The main request teardown.
        """

        for compo_obj in self.components.values():
            compo_obj.finalize()

        other_pages = self.page_request.get_handeled_pages()
        for page_obj in other_pages:
            page_obj.done_request()

        epfltransaction.kill_deleted_transactions(self.request)


    @classmethod
    def get_name(cls):
        if not cls.__name:
            cls.__name = cls.__module__ + ":" + cls.__name__

        return cls.__name

    def __setattr__(self, key, value):
        """ This is the way, the components get thier name:
        By assigning the components as attributes to the page, we can register them here as components,
        and we can tell the components thier id (which is thier attribute-name).
        """

        if isinstance(value, epflcomponentbase.ComponentBase):
            self.add_static_component(key, value)
        # TODO: Check auto instantiation possibility here
        # if isinstance(value, epflcomponentbase.UnboundComponent):
        #     self.add_static_component(key, value(__instantiate__=True))
        else:
            self.__dict__[key] = value # mimic "normal" behaviour

    def add_static_component(self, cid, compo_obj):
        """ Registeres the component in the page. """
        self.__dict__[cid] = compo_obj
        self.components[cid] = compo_obj
        compo_obj.set_component_id(cid)
        compo_obj.set_page_obj(self)


    def has_access(self):
        """ Checks if the current user has sufficient rights to see/access this page.
        """

        if security.has_permission("access", self, self.request):
            return True
        else:
            return False

    def __get_transaction_from_request(self):

        tid = self.page_request.get_tid()
        transaction = epfltransaction.Transaction(self.request, tid)

        if transaction.created:
            transaction.set_page_obj(self)

        return transaction


    def setup_components(self):
        """
        Overwrite this function!
        In this method all components needed by this page must be initialized and assinged to the page (self).
        It is called only once per transaction to register the "static" components of this page.
        No need to call this (super) method in derived classes.
        [request-processing-flow]
        """
        self.root_node = self.root_cls(__instantiate__=True)

    def get_jinja_template_extra_data(self):
        """ Returns the data accumulated by the jinja-epfl-component-extension (jinja_extensions.py).
        There is:

        {
           "compo_js_parts": all javascript-parts of all inlined components on this page.
        }

        """
        return __svc__.jinja.env.epfl_compoext_data[self.template]

    def get_page_init_js(self):
        """ returns a js-snipped which initializes the page. called only once per page """

        opts = {"tid": self.transaction.get_id(),
                "ptid": self.transaction.get_pid()}

        return "epfl.init_page(" + json.encode(opts) + ")"

    def get_template_ctx(self):
        """ Returns a freshly created dict with all the global variables for the template rendering """


        ctx = {"epfl": {},
               "page": self,
               "components": self.components.as_dict()}

        ctx.update(self.components.as_dict())
        ctx.update(self.data)

        return ctx

    def get_template_reflection_info(self):
        """ Returns the reflection info for the template of this page. Duh.
        """
        env = self.request.get_epfl_jinja2_environment()
        return env.get_reflection_info(self.jinja_template)

    def render(self):
        """ Is called in case of a "full-page-request" to return the complete page """

##   todo     self.request.assert_page_access(page_obj=self)

        self.__reopen_overlays() # if any overlays - reopen them!

        self.add_js_response(self.get_page_init_js())

        epflutil.add_extra_contents(self.response, obj = self)

        # pre-render all components
        for component_name, component_obj in self.components.items():
            component_obj.pre_render()

        # exclusive extra-content
        exclusive_extra_content = self.response.get_exclusive_extra_content()

        # main-content
        if exclusive_extra_content:
            out = exclusive_extra_content
        else:
            ctx = self.get_template_ctx()
            out = self.response.render_jinja(self.jinja_template, **ctx)

        return out

    def handle_transaction(self):
        """ This method is called just before the event-handling takes place.
        It calles the init_transaction-methods of all components, that the event handlers have
        a complete setup transaction-state.

        [request-processing-flow]
        """

        for cid, compo in self.components.items():
            if cid + "$__inited__" not in self.transaction:
                self.transaction[cid + "$__inited__"] = True
                compo.init_transaction()

        for cid, compo in self.components.items():
            compo.setup_component()




    def handle_ajax_request(self):
        """ Is called by the view-controller directly after the definition of all components (self.instanciate_components).
        Returns "True" if we are in a ajax-request. self.render_ajax_response must be called in this case.
        A "False" means we have a full-page-request. In this case self.render must be called.

        [request-processing-flow]
        """

        if not self.request.is_xhr:
            return False

        self.handle_transaction()

        ajax_queue = self.page_request.get_queue()
        for event in ajax_queue:

            event_type = event["t"]

            if event_type == "ce": # component-event
                event_id = event["id"]
                cid = event["cid"]
                event_name = event["e"]
                event_params = event["p"]

                component_obj = self.components[cid]
                component_obj.handle_event(event_name, event_params)

            elif event_type == "pe": # page-event
                event_id = event["id"]
                event_name = event["e"]
                event_params = event["p"]

                event_handler = getattr(self, "handle_" + event_name)
                event_handler(**event_params)

            elif event_type == "upl": # upload-event
                event_id = event["id"]
                cid = event["cid"]
                component_obj = self.components[cid]
                component_obj.handle_event("UploadFile", {"widget_name": event["widget_name"]})

            else:
                raise Exception, "Unknown ajax-event: " + repr(event)

        for cid, compo in self.components.items():
            compo.after_event_handling()


        other_pages = self.page_request.get_handeled_pages()
        all_compos = [(self, cid, compo_obj) for cid, compo_obj in self.components.items()]
        for other_page in other_pages:
            all_compos.extend([(other_page, cid, compo_obj) for cid, compo_obj in other_page.components.items()])

        for page_obj, cid, compo_obj in all_compos:
            if compo_obj.is_visible(check_parents = True):
                redraw_parts = compo_obj.get_redraw_parts()
                if redraw_parts:
                    js = "epfl.replace_component('{cid}', {parts})".format(cid = cid,
                                                                           parts = json.encode(redraw_parts))
                    page_obj.add_js_response(js)
            else:
                page_obj.add_js_response("epfl.hide_component('{cid}')".format(cid = cid))


        return True


    def handle_submit_request(self):
        """ Handles the "normal" submit-request which is normally a GET or a POST request to the page.
        This is the couterpart to the self.handle_ajax_request() which should be called first and if it returns
        False should be called.

        Example:

        if page.handle_ajax_request(json):
            return page.response.render_ajax_response()
        else:
            page.handle_submit_request()

        It calls the handle_submit-method of all components in this page.
        """

        self.handle_transaction()

        for component_name, component_obj in self.components.items():
            component_obj.request_handle_submit(dict(self.page_request.params))

        for cid, compo in self.components.items():
            compo.after_event_handling()

    def add_js_response(self, js_string):
        """ Adds the js either to the ajax-response or to the bottom of the page - depending of the type of the request """
        js_string += ";"
        if self.request.is_xhr:
            self.response.add_ajax_response(js_string)
        else:
            self.response.add_extra_content(epflclient.JSBlockContent(js_string))

    def show_fading_message(self, msg, typ = "info"):
        """ Shows a message to the user. The message is non evasive - it will show up and fade away nicely.
        typ = "info" | "ok" | "error"
        """

        js = "epfl.show_fading_message(%s,%s)" % (json.encode(msg), json.encode(typ))

        self.add_js_response(js)

    def show_message(self, msg, typ):
        """
        Displays a simple alert box to the user.
        typ = "info" | "ok" | "error"
        """
        js = "alert(%s)" % (json.encode(msg),)
        self.add_js_response(js)



    def get_css_imports(self):
        """ This function delivers the <style src=...>-tags for all stylesheets needed by this page and it's components.
        It is available in the template by the jinja-variable {{ css_imports() }}
        """
        return self.response.render_extra_content(target = "head")

    def get_js_imports(self):
        """ This function delivers the <script src=...>-tags for all js needed by this page and it's components.
        Additionally it delivers all generated js-snippets from the components or page.
        It is available in the template by the jinja-variable {{ js_imports() }}
        """

        # rendering all JS-parts of the components
        for compo_obj in self.components.values():
            if compo_obj.is_rendered:
                init_js = compo_obj.get_js_part()
                init_js = epflclient.JSBlockContent(init_js)
                self.response.add_extra_content(init_js)

        return self.response.render_extra_content(target = "footer")

    def reload(self):
        """ Reloads the complete page.
        Normally, you only need to redraw the components.
        """
        self.add_js_response("epfl.reload_page();")

    def jump(self, route, **route_params):
        """ Jumps to a new page.
        The target is given as route/route_params.
        The transactions (current an target-page-transaction) are not joined and
        therefore are completely unrelated.
        If you need the data of the current page in the next one (or vice versa), you must
        use "page.go_next(...)" instead.
        """

        target_url = self.request.route_url(route, **(route_params or {}))

        js = "epfl.jump('" + target_url + "');"
        self.add_js_response(js)

    def jump_extern(self, target_url, target="_blank"):
        """ Jumps to an external URL.
        Do not use this to jump to an internal page of this appliaction. Use page.jump instead.
        """

        js = "epfl.jump_extern('" + target_url + "', '" + target + "');"
        self.add_js_response(js)

    def go_next(self, route = None, target_url = None, **route_params):
        """ Jumps to a new page and relates the transactions as parent/child.
        So in the new page-object you can access the current page-object as self.parent .
        The target is given as route/route_params or as target_url.
        E.g. use this in wizards.
        """

        if route:
            target_url = self.page_request.route_url(route, **(route_params or {}))

        js = "epfl.go_next('" + target_url + "');"
        self.add_js_response(js)

    @classmethod
    def get_overlay_options(cls):
        """ This classmethod returns the options for the overlays """
        if cls.overlay_options:
            return cls.overlay_options
        else:
            return {"resizeable": True,
                    "modal": True,
                    "draggable": True,
                    "height": 400,
                    "width": 600,
                    "position": "center"}

    def open_overlay(self, route = None, target_url = None, **route_params):
        """ Opens an overlay. The target is given as route/route_params or as target_url.
        If the route denominates an EPFL-Page, the overlay options will be taken from there.
        The transactions of the new page and the current page are connected as parent/child.
        So in the new page-object you can access the current page-object as self.parent .
        """

        page_class = None

        # getting the target_url and the target-page-obj
        if route:
            page_classes = epflutil.get_page_classes_from_route(self.request, route)
            if page_classes:
                page_class = page_classes[0] # if we have multiple page_objs, just take the first one...

            target_url = self.request.route_url(route, **(route_params or {}))

        if not page_class:
            raise ValueError, "view-controller not found for route '" + route + "'"

        # getting the overlay-opts
        overlay_name = page_class.__name__ # the name is the page-class-name: to be discussed (e.g. multi-window)
        overlay_opts = page_class.get_overlay_options()
        overlay_title = page_class.overlay_title

        # creating the new transaction
        new_transaction = epfltransaction.Transaction(self.request)
        new_transaction.set_pid(self.transaction.get_id())
        new_transaction.set_page_obj(page_class)
        target_url = epflutil.URL(target_url).update_query(tid = new_transaction.get_id()) # adjust the url and add the TID

        # open the overlay
        js = epflclient.make_js_call("epfl.open_overlay", overlay_name,
                                                          target_url,
                                                          overlay_title,
                                                          overlay_opts,
                                                          True)

        self.add_js_response(js)

        # remeber this overlay (for full-page redraw of this parent page)
        self.transaction["overlays"].append({"tid": new_transaction.get_id(),
                                             "name": page_class.get_name(),
                                             "target_url": target_url}) # the url with the TID

    def close_overlay(self):
        """ Closes the current overlay. To be called from the overlay-page it self. """
        overlay_name = self.__class__.__name__ # the name is the page-class-name: to be discussed (e.g. multi-window)
        js = epflclient.make_js_call("epfl.close_overlay", overlay_name)
        self.add_js_response(js)


    def __reopen_overlays(self):
        """ If this page is reloaded (completely) this function reopens its overlays. """

        overlays = self.transaction["overlays"]

        for overlay in overlays:

            transaction = epfltransaction.Transaction(self.request, overlay["tid"])
            page_class = epflutil.get_page_class_by_name(self.request, transaction.get_page_name())
            overlay_opts = page_class.get_overlay_options()
            overlay_title = page_class.overlay_title

            js = epflclient.make_js_call("epfl.open_overlay", overlay["name"],
                                                              overlay["target_url"], # TID is already included
                                                              overlay_title,
                                                              overlay_opts,
                                                              False)

            self.add_js_response(js)

    def handle_CloseOverlay(self, overlay_tid):
        """ Is called by the EPFL, whenever an overlay is closed.
        It is called from the opening page and gives the tid of the overlay to close.
        """

        transaction = epfltransaction.Transaction(self.request, overlay_tid)

        # delete the page itself
        transaction.delete()

        # delete all opened overlays
        overlays = transaction["overlays"]
        for overlay in overlays:
            transaction = epfltransaction.Transaction(self.request, overlay["tid"])
            transaction.delete()



class PageRequest(object):
    """
    A Class containing the request-data specific to a specific page.
    This is an abstraction of the "request"-object provided by the framework.
    The framework's request-object is global, so creating subrequests (needed when handling events
    in page-objects other than the page-object created by the framework's request) can be hard.
    Since all classes of EPFL only rely on this abstraction (page_request) it can be created on the fly
    everytime such a page-object needs one specific to it.
    """

    def __init__(self, request, page_obj):
        self.request = request
        self.page_obj = page_obj
        self.handeled_pages = []
        self.upload_mode = False

        if self.request.content_type.startswith("multipart/"):
            self.upload_mode = True
            self.params = request.params
        elif self.request.is_xhr:
            self.params = request.json_body
        else:
            self.params = request.params

    def is_upload_mode(self):
        return self.upload_mode

    def get_tid(self):
        return self.params.get("tid")

    def get_queue(self):
        if self.upload_mode:
            return [self.params]
        else:
            return self.params["q"]


    def get(self, key, default = None):
        return self.params.get(key, default)

    def getall(self, key):
        return self.request.params.getall(key)

    def __getitem__(self, key):
        return self.params[key]

    def add_handeled_page(self, page_obj):
        """ This page was created and handeled in this request too! """
        self.handeled_pages.append(page_obj)

    def get_handeled_pages(self):
        return self.handeled_pages

    def get_uploads(self):
        if not self.is_upload_mode:
            return {}
        else:
            return {self.params["widget_name"]: self.request.POST[self.params["widget_name"] + "[]"]}



