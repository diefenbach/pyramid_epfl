# coding: utf-8

""" This library contains all epfl-components.

The components must be imported in the namespace of this library.
"""

#: Container
from box.box import Box
from modal_box.modal_box import ModalBox
from recursive_tree.recursive_tree import RecursiveTree

#: Forms
from form.form import Form
from button.button import Button
from text_input.text_input import TextInput
from number_input.number_input import NumberInput
from checkbox.checkbox import Checkbox
from textarea.textarea import Textarea
from texteditor.texteditor import TextEditor
from select.select import Select
from radio.radio import Radio
from buttonradio.buttonradio import ButtonRadio
from simpletoggle.simpletoggle import SimpleToggle
from toggle.toggle import Toggle
from upload.upload import Upload
from download.download import Download
from colorpicker.colorpicker import ColorPicker
from colorthief.colorthief import ColorThief
from datetime_input.datetime_input import DatetimeInput
from autocomplete_input.autocomplete_input import AutoCompleteInput
from password_input.password_input import PasswordInput

#: Visual
from badge.badge import Badge
from diagram.diagram import Diagram
from progress.progress import Progress
from stacked_progress.stacked_progress import StackedProgress
from image.image import Image
from text.text import Text
from placeholder.placeholder import Placeholder
from popover.popover import Popover
from link.link import Link
from breadcrumb.breadcrumb import Breadcrumb
from plain_html.plain_html import PlainHtml

#: Lists
from tabs_layout.tabs_layout import TabsLayout
from nav_layout.nav_layout import NavLayout
from col_layout.col_layout import ColLayout
from cardinal_layout.cardinal_layout import CardinalLayout
from list_layout.list_layout import ListLayout
from pretty_list_layout.pretty_list_layout import PrettyListLayout
from paginated_list_layout.paginated_list_layout import PaginatedListLayout
from link_list_layout.link_list_layout import LinkListLayout
from grouped_link_list_layout.grouped_link_list_layout import GroupedLinkListLayout
from hover_link_list_layout.hover_link_list_layout import HoverLinkListLayout
from context_list_layout.context_list_layout import ContextListLayout, ContextListEntry
from table_layout.table_layout import TableLayout
from selectable_list.selectable_list import SelectableList
from text_list.text_list import TextList

from typeahead.typeahead import TypeAhead

from dropdown.dropdown import Dropdown

from embedded_video.embedded_video import EmbeddedVideo

# Convenience Components
from login_box.login_box import LoginBox


def add_routes(config):
    """
    Called once per thread start, in order to call
    :func:`solute.epfl.core.epflcomponentbase.ComponentBase.add_pyramid_routes` for every component provided by epfl
    through this package.
    """

    Box.add_pyramid_routes(config)
    LoginBox.add_pyramid_routes(config)
    ModalBox.add_pyramid_routes(config)
    TabsLayout.add_pyramid_routes(config)
    NavLayout.add_pyramid_routes(config)
    ColLayout.add_pyramid_routes(config)
    CardinalLayout.add_pyramid_routes(config)
    Link.add_pyramid_routes(config)

    RecursiveTree.add_pyramid_routes(config)
    ListLayout.add_pyramid_routes(config)
    PrettyListLayout.add_pyramid_routes(config)
    PaginatedListLayout.add_pyramid_routes(config)
    LinkListLayout.add_pyramid_routes(config)
    GroupedLinkListLayout.add_pyramid_routes(config)
    HoverLinkListLayout.add_pyramid_routes(config)
    ContextListLayout.add_pyramid_routes(config)
    TableLayout.add_pyramid_routes(config)
    SelectableList.add_pyramid_routes(config)

    TypeAhead.add_pyramid_routes(config)

    Form.add_pyramid_routes(config)
    Button.add_pyramid_routes(config)
    TextInput.add_pyramid_routes(config)
    TextEditor.add_pyramid_routes(config)
    NumberInput.add_pyramid_routes(config)
    Textarea.add_pyramid_routes(config)
    Radio.add_pyramid_routes(config)
    ButtonRadio.add_pyramid_routes(config)
    Toggle.add_pyramid_routes(config)
    SimpleToggle.add_pyramid_routes(config)
    Checkbox.add_pyramid_routes(config)
    Select.add_pyramid_routes(config)
    Upload.add_pyramid_routes(config)
    Download.add_pyramid_routes(config)
    ColorPicker.add_pyramid_routes(config)
    ColorThief.add_pyramid_routes(config)
    DatetimeInput.add_pyramid_routes(config)
    AutoCompleteInput.add_pyramid_routes(config)
    PasswordInput.add_pyramid_routes(config)

    Badge.add_pyramid_routes(config)
    Diagram.add_pyramid_routes(config)
    Progress.add_pyramid_routes(config)
    StackedProgress.add_pyramid_routes(config)
    Image.add_pyramid_routes(config)
    Text.add_pyramid_routes(config)
    Placeholder.add_pyramid_routes(config)
    Popover.add_pyramid_routes(config)
    PlainHtml.add_pyramid_routes(config)
    Breadcrumb.add_pyramid_routes(config)

    TextList.add_pyramid_routes(config)
    Dropdown.add_pyramid_routes(config)

    EmbeddedVideo.add_pyramid_routes(config)
