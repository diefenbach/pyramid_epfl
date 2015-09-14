#* coding: utf-8
from jinja2 import StrictUndefined, TemplateNotFound

from solute.epfl.core.epflpage import Page

import components

from solute.epfl.jinja import jinja_reflection
from solute.epfl.jinja import jinja_extensions
from solute.epfl.jinja import jinja_helpers

from zope.interface import Interface

from solute.epfl.core import (epfltransaction,
                              epflutil,
                              epflpage,
                              epfltempdata,
                              epflmodel,
                              epfli18n,
                              epfll10n,
                              epflassets,
                              epflacl)

from webassets import Bundle
from webassets import Environment

from pyramid.path import AssetResolver


class IEPFLJinja2Environment(Interface):
    pass


epfl_template_cache = {}


# handling extra data in different scopes:

def get_epfl_request_aux(request, param_name, default = None):
    if not hasattr(request, "__epfl_params"):
        setattr(request, "__epfl_params", {})

    params = getattr(request, "__epfl_params")

    return params.get(param_name, default)


def set_epfl_request_aux(request, param_name, value):
    if not hasattr(request, "__epfl_params"):
        setattr(request, "__epfl_params", {})

    params = getattr(request, "__epfl_params")
    params[param_name] = value


# other stuff


def get_epfl_jinja2_environment(request):
    """ This creates a jinja2-environment specific to use with epfl.
    It uses the needed special environment-classes and template-loaders.
    It copies the configuration from the "original"-pyramid-jinja2-environment.
    Safe to call multiple times.
    """

    environment = request.registry.queryUtility(IEPFLJinja2Environment)
    if environment is not None:
        return environment

    oenv = request.get_jinja2_environment()

    loader = jinja_helpers.PreprocessingFileSystemLoader(oenv.loader.searchpath,
                                                         encoding = oenv.loader.encoding,
                                                         debug = oenv.loader.debug, )

    cache_size = int(request.registry.settings.get("jinja2.cache_size", 1000000))

    env = jinja_reflection.ReflectiveEnvironment(loader = loader,
                                                 auto_reload = oenv.auto_reload,
                                                 extensions = oenv.extensions,
                                                 undefined = StrictUndefined, # oenv.undefined,

                                                 block_start_string = oenv.block_start_string,
                                                 block_end_string = oenv.block_end_string,
                                                 variable_start_string = oenv.variable_start_string,
                                                 variable_end_string = oenv.variable_end_string,
                                                 comment_start_string = oenv.comment_start_string,
                                                 comment_end_string = oenv.comment_end_string,
                                                 line_statement_prefix = oenv.line_statement_prefix,
                                                 line_comment_prefix = oenv.line_comment_prefix,
                                                 trim_blocks = True,
                                                 # trim_blocks = oenv.trim_blocks,
                                                 lstrip_blocks = True,
                                                 # lstrip_blocks = oenv.lstrip_blocks,
                                                 newline_sequence = oenv.newline_sequence,
                                                 keep_trailing_newline = oenv.keep_trailing_newline,
                                                 optimized = oenv.optimized,
                                                 finalize = oenv.finalize,
                                                 autoescape = oenv.autoescape,
                                                 cache_size = cache_size,
                                                 bytecode_cache = oenv.bytecode_cache)

    # really shared!
    env.filters = oenv.filters
    env.globals = oenv.globals

    jinja_extensions.extend_environment(env)
    _get_template = env.get_template

    def get_template(*args, **kwargs):
        try:
            if epfl_template_cache[args[0]] is None:
                raise TemplateNotFound(args[0])
            return epfl_template_cache[args[0]]
        except KeyError:
            pass
        try:
            epfl_template_cache[args[0]] = _get_template(*args, **kwargs)
            return epfl_template_cache[args[0]]
        except TemplateNotFound:
            epfl_template_cache[args[0]] = None
            raise


    env.get_template = get_template

    request.registry.registerUtility(env, IEPFLJinja2Environment)
    return request.registry.queryUtility(IEPFLJinja2Environment)


def is_template_marked_as_not_found(request, template_name):

    nfts = request.get_epfl_nodeglobal_aux("not_found_templates", set())

    return template_name in nfts


def mark_template_as_not_found(request, template_name):

    nfts = request.get_epfl_nodeglobal_aux("not_found_templates", set())
    nfts.add(template_name)
    request.set_epfl_nodeglobal_aux("not_found_templates", nfts)


def set_tempdata_provider(config, tempdata_provider):
    config.registry.registerUtility(tempdata_provider, epfltempdata.ITempDataProvider)


def set_nodeglobaldata_provider(config, nodeglobaldata_provider):
    config.registry.registerUtility(nodeglobaldata_provider, epfltempdata.INodeGlobalDataProvider)


def extract_static_assets_from_components(compo_list):
    ar = AssetResolver()

    js_paths = []
    js_name = []
    css_paths = []
    css_name = []

    # The Page needs to be in the webassets first, then all other pages, then all components.
    for cls in compo_list:
        for js in cls.js_name:
            if type(js) is not tuple:
                js = (cls.asset_spec, js)
            if js in js_name:
                continue
            js_name.append(js)
            js_paths.append(ar.resolve('/'.join(js)).abspath())
        cls.js_name = cls.js_name + getattr(cls, 'js_name_no_bundle', [])

        for css in cls.css_name:
            if type(css) is not tuple:
                css = (cls.asset_spec, css)
            if css in css_name:
                continue
            css_name.append(css)
            css_paths.append(ar.resolve('/'.join(css)).abspath())
        cls.css_name = cls.css_name + getattr(cls, 'css_name_no_bundle', [])

    return js_paths, js_name, css_paths, css_name


def generate_webasset_bundles(config):
    compo_bundles = extract_static_assets_from_components(epflutil.Discover.discovered_components)

    page_bundles = []
    pages = [epflpage.Page] + epflutil.Discover.discovered_pages

    for cls in pages:
        page_bundles.append(extract_static_assets_from_components([cls]))

    if config.registry.settings.get('epfl.webassets.active') != 'true':
        return

    ar = AssetResolver()
    epfl_static = ar.resolve('solute.epfl:static')

    my_env = Environment('%s/bundles' % epfl_static.abspath(), 'bundles')

    for i, page in enumerate(pages):
        js_paths, js_name, css_paths, css_name = page_bundles[i]

        js_paths += compo_bundles[0]
        js_name += compo_bundles[1]
        css_paths += compo_bundles[2]
        css_name += compo_bundles[3]

        my_env.register('js%s' % i, Bundle(js_paths, filters='rjsmin', output='epfl.%(version)s.js'))
        my_env.register('css%s' % i, Bundle(css_paths, output='epfl.%(version)s.css'))

        page.js_name += [("solute.epfl:static", url) for url in my_env['js%s' % i].urls()]
        page.css_name += [("solute.epfl:static", url) for url in my_env['css%s' % i].urls()]

        page.bundled_names = js_name + css_name


def includeme(config):
    """
    The main configuration of the EPFL
    """

    config.include('pyramid_jinja2')

    config.add_renderer('.html', 'pyramid_jinja2.renderer_factory')
    config.add_request_method(config.get_jinja2_environment)
    config.add_request_method(get_epfl_jinja2_environment)
    config.add_request_method(set_epfl_request_aux)
    config.add_request_method(get_epfl_request_aux)
    config.add_request_method(epfltempdata.set_epfl_temp_blob)
    config.add_request_method(epfltempdata.get_epfl_temp_blob)
    config.add_request_method(epfltempdata.get_epfl_temp_blob_meta)
    config.add_request_method(epfltempdata.get_epfl_nodeglobal_aux)
    config.add_request_method(epfltempdata.set_epfl_nodeglobal_aux)
    config.add_request_method(is_template_marked_as_not_found)
    config.add_request_method(mark_template_as_not_found)
    config.add_request_method(epflmodel.LazyModelAccessor, name = "epfl_model", reify = True)
    config.add_request_method(epfli18n.get_timezone, name = "epfl_timezone", reify = True)

    config.add_directive("set_tempdata_provider", set_tempdata_provider)
    config.add_directive("set_nodeglobaldata_provider", set_nodeglobaldata_provider)
    config.add_directive("add_epfl_model", epflmodel.add_epfl_model)
    config.add_directive("set_timezone_provider", epfli18n.set_timezone_provider)

    config.add_jinja2_search_path("solute.epfl:templates")
    config.add_jinja2_search_path("solute.epfl.components:")

    # static routes
    config.add_static_view(name = "epfl/static", path = "solute.epfl:static")
    components.add_routes(config)

    config.set_root_factory(epflacl.DefaultACLRootFactory)

    epflassets.EPFLView.configure(config)

    epflutil.Discover()

    generate_webasset_bundles(config)
