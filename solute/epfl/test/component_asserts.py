from solute import epfl
import os
import inspect
import re
from textwrap import wrap
import types

import solute.epfl.test

test_dir = os.path.dirname(inspect.getsourcefile(solute.epfl.test))  #: The directory where all EPFL tests reside.
ignore_tests = False


class AssertBase(object):
    def __init__(self, parent):
        """Registers parent for lookup of attributes not defined on the current object. Used to reflect the error list
            from parent to child.
        """
        self.parent = parent

    def __getattr__(self, item):
        return getattr(self.parent, item)

    def check_type(self, *args):
        """Generates the identification string for the different test types.
        """
        return "{0:<23}{1:<32}".format('%s' % self.compo_name, '[%s]' % "][".join(args))

    def combine_errors(self):
        """Creates a combined string for all entries in the errors list. Handles multi line wrapping and indentation.
        """
        for i, e in enumerate(self.errors):
            if len(e) <= 220:
                continue
            base = e[:55]
            text = wrap(e[55:], 165, subsequent_indent=' ')
            self.errors[i] = "\n".join([base + t for t in text])
        return "\n".join(self.errors)


class AssertStyle(AssertBase):
    def __init__(self, component, result):
        """Contains the following checks:
            * Structure of the general component.
            * Structure of the init method docs.
            * Structure of the general component docs.
           Detected issues will be registered on the global result object.

        :param component: Component class to be tested.
        :param result: Global result object.
        """
        super(AssertStyle, self).__init__(None)

        __tracebackhide__ = True

        self.component = component
        self.compo_name = self.component.__name__

        check_type = self.check_type('style')

        self.errors = []

        AssertStyleStructure(self)

        AssertStyleInit(self)
        AssertStyleDocs(self)

        result['item_count'] += len(self.errors)
        if len(self.errors) > 0:
            result['objects_with_items'] += 1
        self.errors.append(
            '{check_type}New item total: {0} items on {1} objects.'
            .format(result['item_count'], result['objects_with_items'], check_type=check_type)
        )

        assert len(self.errors) == 1, "\n" + self.combine_errors()


class AssertStyleStructure(AssertBase):
    def __init__(self, parent):
        """Asserts for the structure of the general component. Triggers sub checks:
            * Tests present,
            * Package Structure,
            * Dynamic JS format,
            * Static JS format.
        """
        super(AssertStyleStructure, self).__init__(parent)

        __tracebackhide__ = True

        check_type = self.check_type('style', 'structure')

        self.file_path = inspect.getsourcefile(self.component)
        self.file_path = os.path.abspath(self.file_path)

        self.assert_style_structure_tests()

        # TODO: This potentially excludes all those components that define a static folder but do not change the
        # TODO: asset_spec for better compatibility.
        if getattr(self.component, 'asset_spec', None) is None \
                or ':{compo_name}/'.format(compo_name=self.compo_name.lower()) not in self.component.asset_spec:
            return

        self.static_path = os.path.dirname(self.file_path) + '/static'

        self.assert_style_structure_package()

        self.assert_style_structure_dynamic_js()

        if not os.path.exists(self.static_path):
            self.errors.append("{check_type}{compo_name} is missing static folder. ({static_path})"
                               .format(compo_name=self.compo_name, check_type=check_type, static_path=self.static_path))
            return

        self.assert_style_structure_static_js()

    def assert_style_structure_package(self):
        """Contains the following checks:
            * Package files are named correctly.
            * Package path is named correctly.
        """
        __tracebackhide__ = True

        check_type = self.check_type('style', 'structure', 'package')

        # Package files are named correctly.
        package_path = os.path.dirname(self.file_path)
        if not self.file_path.endswith(self.compo_name.lower() + '.py'):
            self.errors.append("{check_type}{compo_name} is missing primary python file."
                               .format(compo_name=self.compo_name, check_type=check_type))

        # Package path is named correctly.
        if not package_path.endswith(self.compo_name.lower()):
            self.errors.append(
                "{check_type}{compo_name} has a malformed package path. Should end with {compo_name_lower} actually is "
                "{package_path}.".format(
                    compo_name=self.compo_name,
                    compo_name_lower=self.compo_name.lower(),
                    package_path=package_path,
                    check_type=check_type,
                ))

    def assert_style_structure_static_js(self):
        """Contains the following checks for the static js:
            * Inheritance calls are present.
            * Inherited initiation calls are present.
            * Registration as epfl component is done properly.
            * Component is inheriting from another epfl component.
        """
        __tracebackhide__ = True

        check_type = self.check_type('style', 'structure', 'js', 'static')

        static_js_file_path = self.static_path + '/{compo_name}.js'.format(compo_name=self.compo_name.lower())
        if os.path.exists(static_js_file_path):
            js_file = file(static_js_file_path).read()

            # Inheritance calls are present.
            r = re.compile("epfl\.{compo_name}\.inherits_from\(epfl\.([A-Za-z]*)\);".format(
                compo_name=self.compo_name))
            result = r.findall(js_file)
            if len(result) != 1:
                self.errors.append(
                    "{check_type}{compo_name} is missing inheritance calls in static js."
                    .format(compo_name=self.compo_name, check_type=check_type))
                return

            # Inherited initiation calls are present.
            if not js_file.count("epfl.{base_compo}.call(this, cid, params);".format(base_compo=result[0])) == 1:
                self.errors.append(
                    "{check_type}{compo_name} is missing inherited initiation call in static js. "
                    "'epfl.{base_compo}.call(this, cid, params);' not found".format(
                        compo_name=self.compo_name, base_compo=result[0], check_type=check_type))

            # Registration as epfl component is done properly.
            if js_file.startswith("epfl.{compo_name} = function(cid, params) ".format(compo_name=self.compo_name)):
                self.errors.append("{check_type}{compo_name} is not correctly created in static js.".format(
                    compo_name=self.compo_name, base_compo=result[0], check_type=check_type))

            # Component is inheriting from another epfl component.
            if not js_file.count("epfl.{compo_name}.inherits_from(epfl.".format(compo_name=self.compo_name)) == 1:
                self.errors.append("{check_type}{compo_name} is not correctly inheriting in static js.".format(
                    compo_name=self.compo_name, base_compo=result[0], check_type=check_type))

    def assert_style_structure_tests(self):
        """Contains the following checks for the tests:
            * testfile is present in the components subdirectory of the tests folder
        """
        __tracebackhide__ = True

        check_type = self.check_type('style', 'structure', 'tests')

        if self.compo_name in ['ComponentBase', 'ComponentContainerBase']:
            return

        file_name = 'test_' + os.path.basename(self.file_path)

        if ignore_tests:
            return

        if not os.path.exists('/'.join([test_dir, 'components', file_name])):
            self.errors.append(
                "{check_type}{compo_name} is missing custom py.test file. ".format(
                    compo_name=self.compo_name, check_type=check_type))

    def assert_style_structure_dynamic_js(self):
        """Contains the following checks for the dynamic js:
            * Component init call is present and well formed.
        """
        __tracebackhide__ = True

        check_type = self.check_type('style', 'structure', 'js', 'dynamic')

        js_file_path = self.file_path[:-3] + '.js'
        if os.path.exists(js_file_path):
            js_file = file(js_file_path).read()
            if not js_file.startswith('epfl.init_component("{{ compo.cid }}"'):
                self.errors.append(
                    '{check_type}{compo_name} has dynamic js missing \'epfl.init_component("{{{{ compo.cid }}}}"\''
                    .format(compo_name=self.compo_name, check_type=check_type))
            if not js_file.startswith('epfl.init_component("{{ compo.cid }}", "%s", {' % self.compo_name):
                self.errors.append(
                    '{check_type}{compo_name} has dynamic js missing \'epfl.init_component("{{{{ compo.cid }}}}", '
                    '"{compo_name}"\''.format(compo_name=self.compo_name, check_type=check_type))


class AssertStyleInit(AssertBase):
    def __init__(self, parent):
        """Asserts for the init method documentation of the component. Contains the following checks:
            * Docstring present.
            * Required parameters present and in the correct position.
            * All inherited parameters present or exempted.
            * All inherited docstrings correct.
            * Function parameters have docstrings as required.
            * All defaults are None.
        """
        super(AssertStyleInit, self).__init__(parent)

        __tracebackhide__ = True

        check_type = self.check_type('style', 'init')

        init_func = self.component.__init__
        init_docs = init_func.__doc__
        init_code = init_func.func_code

        # Both bases are exempt from these requirements, since they do not have an API to be exposed in this fashion.
        if self.component in [epfl.core.epflcomponentbase.ComponentBase,
                              epfl.core.epflcomponentbase.ComponentContainerBase]:
            return

        base = self.component.__bases__[0]
        base_init_func = base.__init__
        base_init_docs = base_init_func.__doc__
        base_init_code = base_init_func.func_code

        # Docstring present.
        if not init_docs:
            self.errors.append("{check_type}{compo_name} __init__ method has no doc string."
                               .format(compo_name=self.compo_name, check_type=check_type))
            return
        if not base_init_docs:
            self.errors.append("{check_type}{compo_name}'s parent __init__ method has no doc string."
                               .format(compo_name=self.compo_name, check_type=check_type))
            return

        # Required parameters present and in the correct position.
        for position, name in [(0, 'self'), (1, 'page'), (2, 'cid'), (-1, ('extra_params', 'kwargs'))]:
            if init_code.co_varnames[position] == name:
                continue
            if type(name) is tuple:
                if init_code.co_varnames[position] in name:
                    continue
                name = "' or '".join(name)

            self.errors.append("{check_type}{compo_name} __init__ method is missing or misplacing parameter '{name}'."
                               .format(compo_name=self.compo_name, name=name, check_type=check_type))

        # All inherited parameters present or exempted.
        base_varnames = set(base_init_code.co_varnames).difference(getattr(self.component, 'exempt_params', []))
        # Get the varnames not present in both.
        missing_varnames = base_varnames.difference(init_code.co_varnames)
        # Remove standard varnames.
        missing_varnames = missing_varnames.difference(['self', 'args', 'kwargs', 'page', 'cid'])
        # Reduce to the varnames only present in the parent.
        missing_varnames = missing_varnames.intersection(base_init_code.co_varnames)

        if len(missing_varnames) > 0:
            self.errors.append("{check_type}{compo_name} __init__ method is missing the following inherited parameters:"
                               " {params}"
                               .format(compo_name=self.compo_name, params=missing_varnames, check_type=check_type))

        base_init_docs_dict = {}
        for line in base_init_docs.split("\n"):
            line = line.strip()
            if not line.startswith(':param '):
                continue
            line_name = line[7:].split(':')[0]
            base_init_docs_dict[line_name] = line

        # All inherited docstrings correct.
        for varname in base_varnames.intersection(init_code.co_varnames):
            if base_init_docs_dict.get(varname, '') in init_docs:
                continue
            self.errors.append("{check_type}{compo_name} __init__ method has wrong docstring for inherited parameter "
                               "{param}."
                               .format(compo_name=self.compo_name, param=varname, check_type=check_type))

        # Function parameters have docstrings as required.
        for var in init_code.co_varnames:
            if var in ['self', 'page', 'args', 'kwargs', 'extra_params', 'cid']:
                continue
            if ":param {var}:".format(var=var) not in init_docs:
                self.errors.append(
                    "{check_type}{compo_name} __init__ method is missing docs for {param}."
                    .format(compo_name=self.compo_name, param=var, check_type=check_type)
                )

        # All defaults are None.
        argspec = inspect.getargspec(init_func)
        argspec_offset = len(argspec.args) - len(argspec.defaults)
        if any(v is not None for v in argspec.defaults):
            self.errors.append(
                "{check_type}{compo_name} __init__ method has defaults that are not set to None. {debug}"
                .format(compo_name=self.compo_name, check_type=check_type, debug=dict([
                    (argspec.args[i + argspec_offset], v) for i, v in enumerate(argspec.defaults) if v is not None
                ]))
            )


class AssertStyleDocs(AssertBase):
    def __init__(self, parent):
        """Asserts for the general documentation of the component. Contains the following checks:
            * Only valid attributes are present.
            * All custom attributes have a docstring.
            * All custom attribute docstrings are formatted correctly.
        """
        super(AssertStyleDocs, self).__init__(parent)

        __tracebackhide__ = True

        check_type = self.check_type('style', 'docs')

        source, starting_line = inspect.getsourcelines(self.component)

        custom_attributes = re.compile('^    [a-zA-Z_]* = .*$')
        doc_line = re.compile('^    #: .*$')
        for line_number, line in enumerate(source):
            abs_line_number = line_number + starting_line + 1
            search_result = custom_attributes.findall(line)
            if not search_result:
                continue
            attr_name = search_result[0].strip().split(' ', 1)[0]

            # Watchdog if for "All custom attributes have a docstring.", attributes listed here are exempt from this
            # check due to them being core attributes.
            if attr_name in ['asset_spec', 'compo_state', 'theme_path', 'css_name', 'js_name', 'js_parts',
                             'new_style_compo', 'compo_js_params', 'compo_js_extras', 'compo_js_name', 'template_name',
                             'compo_config', 'data_interface', 'default_child_cls', 'auto_update_children',
                             'theme_path_default', 'js_name_no_bundle']:
                continue

            # Only valid attributes are present.
            if attr_name in ['cid', 'slot']:
                self.errors.append(
                    "{check_type}Invalid attribute set: 'slot' and 'cid' are reserved names. (Line: {line_number})"
                    .format(line_number=abs_line_number, check_type=check_type))
                continue

            # All custom attribute docstrings are formatted correctly. First look behind the attribute.
            attr_tail = search_result[0].strip().split(' ', 2)[2]
            if '#' in attr_tail:
                if '  #: ' not in attr_tail:
                    self.errors.append(
                        "{check_type}Bad format on docstring for {attr_name}. Expected string containing '  #: ', got"
                        " '{attr_tail}' instead. (Line: {line_number})".format(
                            attr_name=attr_name,
                            attr_tail=attr_tail,
                            line_number=abs_line_number,
                            check_type=check_type))
                continue

            line_cursor = 1
            current_line = source[line_number - line_cursor]
            # No doc string yet, so look backwards.
            if not doc_line.match(current_line):
                self.errors.append(
                    "{check_type}No docstring found for {attr_name}. Expected a line starting with '#: ', got "
                    "'{current_line}' instead. (Line: {line_number})".format(
                        attr_name=attr_name,
                        current_line=current_line.strip(),
                        line_number=abs_line_number - line_cursor,
                        check_type=check_type))

            while current_line.strip().startswith('#') and line_cursor <= current_line:
                if not doc_line.match(current_line):
                    self.errors.append(
                        "{check_type}Bad format docstring found for {attr_name}. Expected a line starting with '#: ', "
                        "got '{current_line}' instead. (Line: {line_number})"
                        .format(
                            attr_name=attr_name,
                            current_line=current_line.strip(),
                            line_number=abs_line_number - line_cursor,
                            check_type=check_type
                        )
                    )
                    break
                current_line = source[line_number - line_cursor]
                line_cursor += 1


class AssertRendering(AssertBase):
    def __init__(self, compo_info, html, js, result):
        """Contains the following checks:
         * An element with the appropriate epflid exists in the generated html.
        """
        super(AssertRendering, self).__init__(None)

        __tracebackhide__ = True

        self.component = compo_info['class'][0]
        self.compo_name = self.component.__name__

        check_type = self.check_type('rendering')

        cid = compo_info['cid']

        # TODO: Create appropriate checks for the generated javascript.
        assert html.count(' epflid="{cid}"'.format(cid=cid)) == 1, \
            '{check_type}The element with the cid "{cid}" is missing in the generated HTML:\n{html}' \
                .format(cid=cid, html=html, check_type=check_type)


class AssertCoherence(AssertBase):
    def __init__(self, component, compo_info, result):
        """Contains the following checks:
         * Coherence of object instance attributes to transaction compo_info.
         * Coherence of object instance compo_info to transaction compo_info.
         * Coherence and writeability of object instance compo_state attributes into/to transaction compo_info.
        """
        super(AssertCoherence, self).__init__(None)

        __tracebackhide__ = True

        self.component = component
        self.compo_name = compo_info['class'][0].__name__

        check_type = self.check_type('coherence')

        # Coherence of object instance attributes to transaction compo_info.
        assert self.component.slot == compo_info['slot'], \
            "{check_type}slot attribute differs in transaction and instance".format(check_type=check_type)
        assert self.component.cid == compo_info['cid'], \
            "{check_type}cid attribute differs in transaction and instance".format(check_type=check_type)
        assert self.component.__unbound_component__.__getstate__() == compo_info['class'], \
            "{check_type}class attribute differs in transaction and instance".format(check_type=check_type)

        # Coherence of object instance compo_info to transaction compo_info.
        assert self.component._ComponentBase__config == compo_info['config'], \
            "{check_type}config not stored correctly in transaction".format(check_type=check_type)

        # Coherence and writeability of object instance compo_state attributes into/to transaction compo_info.
        for name in self.component.combined_compo_state:
            attr_value = getattr(self.component, name)
            if isinstance(attr_value, types.MethodType):
                continue
            try:
                setattr(self.component, name, attr_value)
            except:
                import pdb

                pdb.set_trace()
                raise
            assert compo_info['compo_state'][name] == attr_value, \
                "{check_type}compo_state not stored correctly for {name}. Should be {attr_value} actually is" \
                " {state_value}".format(
                    name=name,
                    attr_value=attr_value,
                    state_value=compo_info['compo_state'][name],
                    check_type=check_type
                )
