from solute.epfl import epflpage


class BasePage(epflpage.Page):
    pass


class PageWithJS(BasePage):
    js_name = BasePage.js_name + ['example.js']


class PageWithJSNoBundle(PageWithJS):
    js_name_no_bundle = PageWithJS.js_name_no_bundle + ['no_bundle_example.js']


class PageWithCSS(BasePage):
    css_name = BasePage.css_name + ['example.css']


class PageWithCSSNoBundle(PageWithCSS):
    css_name_no_bundle = BasePage.css_name_no_bundle + ['no_bundle_example.css']


class PageWithCSSandJS(BasePage):
    js_name = BasePage.js_name + ['example.js']
    css_name = BasePage.css_name + ['example.css']


class PageWithCSSandJSNoBundle(PageWithCSSandJS):
    js_name_no_bundle = PageWithJS.js_name_no_bundle + ['no_bundle_example.js']
    css_name_no_bundle = BasePage.css_name_no_bundle + ['no_bundle_example.css']


class PageWithEventHandler(BasePage):
    counter = 0

    def handle_increase_counter(self, counter=None):
        if counter is None:
            self.counter += 1
        else:
            self.counter = counter
