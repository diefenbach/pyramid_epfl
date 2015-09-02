import pytest
from solute.epfl import components
import re


@pytest.fixture(params=[True, False])
def bool_toggle(request):
    return request.param


def test_label(page):
    page.root_node = components.Box(
        node_list=[
            components.Button(
                cid='button',
                event_name='test_event'
            ),
            components.Button(
                cid='button_with_label',
                event_name='test_event',
                label='test_label'
            )
        ]
    )

    page.handle_transaction()

    assert '<label ' not in page.button.render()
    assert '<label ' in page.button_with_label.render()
    assert '>test_label<' in page.button_with_label.render()


def test_value(page, bool_toggle):
    icon = None
    if bool_toggle:
        icon = 'times'

    page.root_node = components.Box(
        node_list=[
            components.Button(
                cid='button',
                event_name='test_event',
                value='test value',
                icon=icon
            )
        ]
    )

    page.handle_transaction()

    assert 'test value' in page.button.render()

    page.button.reset_render_cache()
    page.button.value = None

    assert 'test value' not in page.button.render()


def test_icon(page, bool_toggle):
    label = None
    if bool_toggle:
        label = 'some label'

    page.root_node = components.Box(
        node_list=[
            components.Button(
                cid='button_with_icon',
                event_name='test_event',
                icon='times',
                label=label
            ),
            components.Button(
                cid='button_with_icon_size',
                event_name='test_event',
                icon='times',
                icon_size=3,
                label=label
            ),
            components.Button(
                cid='button_with_icon_color',
                event_name='test_event',
                icon='times',
                icon_color='primary',
                label=label
            ),
            components.Button(
                cid='button_with_icon_size_color',
                event_name='test_event',
                icon='times',
                icon_size=3,
                icon_color='primary',
                label=label
            ),
        ]
    )

    page.handle_transaction()

    assert 'fa fa-times' in page.button_with_icon.render()
    assert 'fa-3x' not in page.button_with_icon.render()
    assert 'text-primary' not in page.button_with_icon.render()

    assert 'fa fa-times' in page.button_with_icon_size.render()
    assert 'fa-3x' in page.button_with_icon_size.render()
    assert 'text-primary' not in page.button_with_icon_size.render()

    assert 'fa fa-times' in page.button_with_icon_color.render()
    assert 'fa-3x' not in page.button_with_icon_color.render()
    assert 'text-primary' in page.button_with_icon_color.render()

    assert 'fa fa-times' in page.button_with_icon_size_color.render()
    assert 'fa-3x' in page.button_with_icon_size_color.render()
    assert 'text-primary' in page.button_with_icon_size_color.render()


def test_tooltip(page):
    page.root_node = components.Box(
        node_list=[
            components.Button(
                cid='button',
                event_name='test_event'
            ),
            components.Button(
                cid='button_with_tooltip',
                event_name='test_event',
                tooltip='test tooltip'
            )
        ]
    )

    page.handle_transaction()

    assert 'title=""' in page.button.render()
    assert 'title="test tooltip"' in page.button_with_tooltip.render()


def test_button_size_and_color(page, bool_toggle):
    color = None
    if bool_toggle:
        color = 'default'

    page.root_node = components.Box(
        node_list=[
            components.Button(
                cid='button',
                event_name='test_event',
                color=color
            ),
            components.Button(
                cid='button_sm',
                event_name='test_event',
                button_size='btn-sm',
                color=color
            ),
            components.Button(
                cid='button_md',
                event_name='test_event',
                button_size='btn-md',
                color=color
            ),
            components.Button(
                cid='button_lg',
                event_name='test_event',
                button_size='btn-lg',
                color=color
            )
        ]
    )

    page.handle_transaction()

    btn = page.button
    btn_sm = page.button_sm
    btn_md = page.button_md
    btn_lg = page.button_lg

    color_set = re.compile('class="[^"]*btn-default[^"]*"')

    if bool_toggle:
        assert color_set.search(btn.render())
        assert color_set.search(btn_sm.render())
        assert color_set.search(btn_md.render())
        assert color_set.search(btn_lg.render())
    else:
        assert not color_set.search(btn.render())
        assert not color_set.search(btn_sm.render())
        assert not color_set.search(btn_md.render())
        assert not color_set.search(btn_lg.render())

    no_size = re.compile('class="[^"]*form-control[^"]*"')
    sm = re.compile('class="[^"]*btn-sm[^"]*"')
    md = re.compile('class="[^"]*btn-md[^"]*"')
    lg = re.compile('class="[^"]*btn-lg[^"]*"')

    assert no_size.search(btn.render())
    assert not sm.search(btn.render())
    assert not md.search(btn.render())
    assert not lg.search(btn.render())

    assert not no_size.search(btn_sm.render())
    assert sm.search(btn_sm.render())
    assert not md.search(btn_sm.render())
    assert not lg.search(btn_sm.render())

    assert not no_size.search(btn_md.render())
    assert not sm.search(btn_md.render())
    assert md.search(btn_md.render())
    assert not lg.search(btn_md.render())

    assert not no_size.search(btn_lg.render())
    assert not sm.search(btn_lg.render())
    assert not md.search(btn_lg.render())
    assert lg.search(btn_lg.render())


def test_is_submit(page):
    page.root_node = components.Box(
        node_list=[
            components.Button(
                cid='button',
                event_name='test_event',
                is_submit=False
            ),
            components.Button(
                cid='button_is_submit',
                event_name='test_event',
                is_submit=True
            )
        ]
    )

    page.handle_transaction()

    assert 'type="button"' in page.button.render()
    assert 'type="submit"' in page.button_is_submit.render()


def test_disabled(page):
    page.root_node = components.Box(
        node_list=[
            components.Button(
                cid='button',
                event_name='test_event',
                disabled=False
            ),
            components.Button(
                cid='button_disabled',
                event_name='test_event',
                disabled=True
            )
        ]
    )

    page.handle_transaction()

    disabled = re.compile('class="[^"]*disabled[^"]*"')

    assert disabled.search(page.button_disabled.render())
    assert not disabled.search(page.button.render())
