import pytest
from solute.epfl import components


def test_render_carousel(page):
    page.root_node = components.Carousel(
        width=400,
        height=200,
        entries=["image1.png", "image2.png", "image3.png"]
    )
    page.handle_transaction()

    compo = page.root_node

    print compo.render()

    assert 'class="carousel slide"' in compo.render(), "carousel class not found"
    assert 'width:400px' in compo.render(), "width not found"
    assert 'height:200px' in compo.render(), "height not found"
    assert 'class="carousel-indicators"' in compo.render(), "carousel indicator class not found"
    assert 'class="carousel-inner"' in compo.render(), "carousel inner class not found"
    assert 'class="left carousel-control"' in compo.render(), "carousel left control class not found"
    assert 'class="right carousel-control"' in compo.render(), "carousel right control class not found"
    assert 'src="image1.png"' in compo.render(), "image1 not found"
    assert 'src="image2.png"' in compo.render(), "image2 not found"
    assert 'src="image3.png"' in compo.render(), "image3 not found"


def test_render_carousel_without_size(page):
    page.root_node = components.Carousel(
        entries=["image1.png", "image2.png", "image3.png"]
    )
    page.handle_transaction()

    compo = page.root_node

    print compo.render()

    assert 'class="carousel slide"' in compo.render(), "carousel class not found"
    assert 'width' not in compo.render(), "width not found"
    assert 'height' not in compo.render(), "height not found"
    assert 'class="carousel-indicators"' in compo.render(), "carousel indicator class not found"
    assert 'class="carousel-inner"' in compo.render(), "carousel inner class not found"
    assert 'class="left carousel-control"' in compo.render(), "carousel left control class not found"
    assert 'class="right carousel-control"' in compo.render(), "carousel right control class not found"
    assert 'src="image1.png"' in compo.render(), "image1 not found"
    assert 'src="image2.png"' in compo.render(), "image2 not found"
    assert 'src="image3.png"' in compo.render(), "image3 not found"
