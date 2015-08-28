# * encoding: utf-8
from __future__ import unicode_literals
from lxml import etree

from solute.epfl import components
import base64


# Fixtures
###############################################################################


IMAGE_BASE_64_BROWSER = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAG4AAABuCAYAAADGWyb7AAAABHNCSVQICAgIfAhkiAAAD+9JREFUeJztnVusXUUZx39fz8Hueq00SiGijb54iykUYitEDkrQN1tiyilQNDGBamJiAg8kFrMbbwXUqCRSTQzxgh5ItKcPxsjl9AjBtkDTY0h88QUKcomptELtPrR0fJiZtWbNmpm19j5771Yz/6TdZ6+5rFnzzX++y8yaDRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRn9Qc50A/5HsAyYBCaGXO9p4BTwRr8Fs+CacQ5wLvBe4B1oIQ4Dp4FjwGHgX8DJfgpnwYVhGXYOsAr4OHAlWniTQ7rHKbTQ9gL7gJfpQ3jDasT/E1yGrQLWoIX2cXN9WNPlaeAI8E70QHmcPoR3tgpu3DolxrA15rsV4jlDbs9y4HLKma+18M5GwY1bp6QYZoU1ikFk730ecJlzrZXwzrTgfGYtYzw65QBaeIo+Gbbsgdd1Kc86EECJ1IyG2z+oP7s/ubeacM9N9q+BhHcmBRdi1qT5Pkqdssr8O2yuu/drZphSIHWbTgESEGhLuMJTpq2PAf8k4iqM26psstaWoYU4Kp1yEi28w+hpk6b7yf2L+tNe2HLMz2JzIqKAnwZTb7/9cgC63R95KbN++14A/gjcC/wVWAzVN07GtbXWJhitTnkX2pKzI7nV/RSGaFFWqURaX+1bBVwIvJ2Efh8145ZsrR0/ftz5Zkd1vdmCgMDkpB6L995b1Sk33XRTrUwQMz3EnQqndzo3EVCqml42AFGgkMBMKqa4Yvv2RuadQE+TPzCf/wk1c5SMG7q1JqkhLQrUkMZh6japWwSMk6JCEdQQeTJswQ3MsNdee83rFP1liqniu06PmXSadfOn5gHYunUrUDLQR42BMz1d1ZY7Eo+nzEfdQNFsc9m4rVZaFEDHfJvyUmfpB8MU3NIZZkgTGrcl2wKjVllzfGkPUIyL4ot/H/GE4yaJEV69qFWNabr2h2EJzpqz64FP0ZJhLgpmKeIdk5jDpnZcCSi6dIPp3R07EGBiQo+bPXv2APCHrb/TGaZ3GpnFpjtAVDxVeaVnVjptt2wDjF/Hy2+ulr8ndtMwhiE4K7RPAJuADbRiWMTIiI1KpYIOrlc6fFU8NqVqsLRJ3CnKqkj7JF3dQFhqdb7QLgNWE2DYulfXlTeNCUdAlMRbFUif6k4BsPDXBTPawwNi7UUXIUC32wWg0zmqExxm2JtEZ7RQ+6aPmqRdFHwUcHWcK9Tt25cD0O3+3Kv8a/aPE+jIyY/RVuWrBJzwpcQBWwutAtO3wcHf4AdJSompVAVmmm1inKFlKptOrecoSBpUwVJMpS2wDO1nfhj4KNrvrPXpoFNlo9DWvbqu3o0C82oeV49Y3TaPue5ZbFOu9eVMY0/MzgPwxFqTtpaw8jcD5U8maadlmsX00UABv+FORRE6CtuMub/LXNnlZfiyV2LefE75VU0C70P36/uBhwms1w0iuJZMCyhyI0mJDT7ji0XCgSZ6EZ9m40iGPKo5RUX8LW26xmuwxlMkNfZQdUygGfcxdL/aCEol8Nyv4BqFdvG/LwbqYpsvRli1C+31KaaiFiXAk2+xfo5Nf3MwXxwvtcgjTuN8Qe8yl6vMm92/zZTUxhNsCxgu1o2AD5ynrx05NVXJc/e3Kl8ngBXABUTW6/oRXEum6QeLmu6NYfSlB/wGh3Lu7jnYGDUV8TOt+g0xK+b7tUB01aCt4FozDfRDzvPniggKXSbz+sFN4pQ3x+vLiiffsqdy/dLjmxBxrMiFqwF48MEHWz5CyrN2ULPdta7avX9bMSTdLBvXO0Wjs3ipH2b362D/ZzbeAMAHzlseLHP3twor0/b9BuAo8CzwShursk/rsZzng89RDM1AmoRHe1lvC8swiRY6rrhXOFUilqMuFZ4tCjt18NBObdWgiXF9MQ20zpIAkyyu5ArzV/UhnnqrG6sTLj2+MVg+5eaF8SJO0Cngt9XrRwmyRa8KWB22cT0Fa2JhAClCJF66lKsGLkMBZg+8jijFV27+EgAfulD7d1/d/kOgwrwJdL9PAJJi3GB+GkRHlumTlO1Fk1iiFmm6Qf1lj6pfacGasF5PlRrkkWKMa8G0iyoPYa3DHd0uSuAKprSu686XtdrRjOKpt+3GfZxLXtvouFCRedQZzGvXrq2klrruxXDZmXcAwuwa32+rYtOGXaCE2QMO05yWquL/uu3ozga9XprZMfzsZ+2s5RDjJtDz6XoamBaKMdgAhgQiBcpOJRFFoa8601qt5sjYbDV3tptgFaXFH7q71IwXW/2SlG/fCDFuEq0EP4W2ZCpCO3ZM77m4Uk0BUjDNxgAXFhYoOOM838G3uX5Y/SFvW9Dpn7/c7tn4ZrDBT/Ckd+UF73uIDaqIkGyM6bjpnSAwu28bIlLTRWXdBOqn5t+NGiHGTVKup60iJFyjbIMMEB19SI/AUT5cyj9sKFlkSeSNKWkZ2FcbCL5QrNm5hnJpRqBkmo5wCPPsRcRnGpgYAtZ0LplmYZ761+/0rh+l2un/iDQ51jn+QNoVzjPtX+sCMLtfR1Y2rY+v/enNQqu9yyYi41j8ArBxoVK2Yc8DXPtu/efdhxP5SriMs7qteTOqHV2REH+8jeJ9RpKjaLLNIkZN8dnMujKSH/LHSMwkqWVe01fRFYL+9eOk9/eFVLcbFIugrl8mSjTTxGWa0wwFc3OPJBpYqPpKasWguS+ii+youM63DnfV6qveEy+9C5RMc63HsMW/GlFCb7EHCJ1Op5JaxioNZqtWb2uceG/1e2Rzmsu4Zt1moCThmAgtFXRgRDfMJuXGxmjLGtLaLIEntidEVw7a3H+4sMKJ67ajxyoxRRsrPLSwEHzIuUfmzF+HCUr3Vyurl2/QEYrPFxciHXOd0YG/8Zno6rLUaLLoAi7TVldyKmPz+zX1ej2bwxthq83Vl7D6vWmDxTCwjCbdFht80rRLsKkTg6YZaWYMOqL7KxdTY4X3GXw0bdCMQ2igBdSg264AxInKL5hmUpkS5+ZcpgXwK8OUrd8F4KqrDujvV+mPhx9+2GS8vVrueqvLjFAL3WaZts1JB71dKtR5XaBk2mfX6nK9Xj0mKiJ0OrMmvVdcVyKsMLrNlrP5ijZY1V2zKt02egkCbO7fqvRftPB0W5w54YGZYlSZ3j93mkqEDZ5+UW66Dd1CgVKRXSmq3HcSLJuKCPUPKyS7A3mZvfXRo3pkd7t6P6JvPdqY3dzcXnPlsJPitL5gmtZlV336AErgjp3Onnzgkksuqbbs+lhM0WeaC3Gu73KutUensweFYrG36F3vIMCJxU2xmZJC/wljtSrrbZHIPgqp/eEhPoraeFKDYfCISTV3XE/pxfvIPKNMoG9MwZOoyT8lU6BExyQDob+9e5t0mo7GW6bBtwHYufMpvSEnGtbzd0NZ2BjmzVQaVFiZptO2+EzdAcStSB+Lxk+zqPprEnV1xr3hIv7+lTJabKDWmEJBspbhsDBSFuXo/SQV1UXNXaGI6b/hI+Fk6wjJoUOHKsHTvXutTns2Ua1pvIBl2i233ALAb++fQRCmr50eYFAUBnnBtN+b9bVrnvFjn2GErEgXnU4HkdKatJ+dTse4bxFuCdXFb9eqdMMxflE7Tq41278GiFVW67N9n+zcQego5ZpXX3U2RE2a6dCIwmKP+XHKMjKS5g6s2r0jKyblIl9faGBcOYRqTPvFSudJgRuNLvvlbfpz605CD2E3I98/MxO+8X0rdYYbQv6a6HQpmVZgyyve/bRu273/RUSJ9tsa+kcBvd7nEFXGIl3mCbB8xQqEOnMLV8B22ZmyKludIJAcxWFnU0l0Ja+stClm2Q9shKptOT+iVUlqeAchUXbYiDLu0EoTEfiF0R1fDGQS4QEz8jdbpt3oM+3rAHz/+9+uFL311lvDN74+cqrBfVWdZnHNM9aqjO8lEZQX4WiAE6t0mSdA78Ri5bp7l+gbsyNAwo9riimOGY3NifO4/YsyYv4Ps0rZ2SA4mZz5PScG5hXJLxjdUkE5mW82Vx541Iz4R3XkYvOzK71yVvfpKP/3vvcer87nzWd6xF7zjLe6UFmXE+B8AHbv07u9Nm2waW3eHbABkLojba3NE71FLyhhV8Ct1Wg+Q7HK6KZQWdIKeJ9oUEQDu11RBUPhZI8IlrhhV85hY9AdaHjg/nfyJmEZZ0+VO00x5G3Ew97tu17R6sjY/MlKKykP7vFh63s+km4f3jLSrhaYB7cMq63LNUE/lt3vaN9Idb9bkQjQW6zms/s1O8tXhAXgC2YMVqU9Ve459HFJp9rdIUUnO2QHjYYHeyZRZ9s2Nd83tTVEWX8sWFSh2ivTJWMSLajngDn0C3WXoXcxm72UPtMswmdWlWhypMPugt1PefDgQQBmjL931/XWWr1ZZ63tObkACOk2i3Sn9npad67oHEvmVfJytOXFRqMxbNObRL8YfgT9uqrVeZ7wBkFMOEsdlYN2Sotyquz4UOu1cMLPpVT6OI9hw+q4k+g3HR930hqE951Rtqtg2vS03ggpMoNScNddof2SAN8ARO/9D0J3qO9+1dwxk29Fp35VL+uEjYzikhgr3I9VpgQqwOb+YpWuOzCA8MaHZvXRJtzSghESthyTq9tYS1QIruUVscrhsdH340LC28BwD/wMoXYGs7/ivmXLtJnF7q8VLqz35AExLTpNSl0VrkeKfMFUgWJhf8RWZcgBd4V3GniF4R6x62MCWAmsMZ/BAaKFFjZs7JWClV7Hth7wSprdrWgQNxHDHAFiwrDCewy9HDDMQ619vAn4CLARfUREB5CHHnqollFvDdCdZnVfJS0inVL/NLOufF87Uk+qDhGmt+hIiqs7y6BJvWyLk4Ys3sDxtVMsOok+E/gVRjtNvgkdIX4/Ol51PiGdWryrELHqgNjbMqlpNJw7Uo8QPa9EDOVD53mljJqWOIk+/NseSXy6afp7gwF+96VPLAJ/Bx5Cv5heMYgK5ok9dQhibAifzppmYy1vU0yR2OtU/um1Vcb4m5D6YJqd/fahfe3DwKkzfXw9tPUjYwrMQezYXxvVbxJbmZ7YnkD45KMi8BxxACVVbxxWaH9Bn0S6H91Xb4zHW2wH9zAW+wpz1BW5+uqrK9/jr/hi57iIrVjPHj+vy/wfuw3ldG118J133lnJ9/TTTze2wcAV2m60sfgSAx4JNUoszY9MBmoKuzOSyYE0hK0il60eHVLIKym0RDPOKHzm2YNL7XsOozSUxonY7/zYH7bYh54ea0KDs4txFiE/cg3lUcHnchZEcpaImpXopNmfkplD67Sa0ODsZJyFfWdv1D8HNm5YRh1A/87PYapLae6PNx0h8vs6ZyPjLFw/8hzgb+gHOcJoIzmjRujHmfzp0jrbUVfsbGacD5eBo4zkjBqtGNWE/yXBwWh/d2ecaGRURkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGxrDxX9vSDGHY9HEvAAAAAElFTkSuQmCC"
IMAGE_BASE_64_SERVER = "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"


# Assert Helper
###############################################################################
def assert_outer_div(compo, height=None, width=None, mandatory=None):
    compo_html = etree.fromstring(compo.render())

    assert compo_html.attrib.get('epflid', None) == "%s" % compo.cid, "epflid not found"
    assert compo_html.attrib.get('id', None) == "%s" % compo.cid, "id not found or wrong"
    assert "epfl-upload" in compo_html.attrib.get('class', None), "mandatory class not found"

    assert "epfl-upload" in compo_html.attrib.get('class', None), "class not found or wrong"
    if height is not None:
        assert "height:%spx;" % height in compo_html.attrib.get('style', None), "height not set correct"
    if width is not None:
        assert "width:%spx;" % width in compo_html.attrib.get('style', None), "width not set correct"

    if mandatory:
        assert "mandatory" in compo_html.attrib.get('class', None), "mandatory class not found"


def assert_file_input(compo, name=None):
    compo_html = etree.fromstring(compo.render())
    file_input = compo_html.find(".//input[@type='file']")
    assert file_input is not None, "No file input found"
    if name is not None:
        assert file_input.attrib.get("name", None) == "test_upload", "name not set or not correct"


def assert_no_file_input(compo):
    compo_html = etree.fromstring(compo.render())
    file_input = compo_html.find(".//input[@type='file']")
    assert file_input is None, "file input found but file input was not expected"


def assert_dropzone(compo, drop_zone_add_position_top=None, drop_zone_add_text=None):
    compo_html = etree.fromstring(compo.render())
    dropzone = compo_html.find(".//div[@class='epfl-dropzone text-center']")
    assert dropzone is not None, "dropzone not found"
    dropzone_outer_div = dropzone.find('div')
    assert dropzone_outer_div is not None, "dropzone outer div not found"
    if drop_zone_add_position_top is not None:
        assert dropzone_outer_div.attrib.get("style", None) == "position:relative; top: {0}%".format(
            drop_zone_add_position_top), "dropzone add position top"
    if drop_zone_add_text is not None:
        dropzone_inner_div = dropzone_outer_div.find('div')
        assert dropzone_inner_div is not None, "dropzone inner div not found"
        assert dropzone_inner_div.text == drop_zone_add_text, "dropzone add text not correct"


def assert_no_dropzone(compo):
    compo_html = etree.fromstring(compo.render())
    dropzone = compo_html.find(".//div[@class='epfl-dropzone text-center']")
    assert dropzone is None, "dropzone found but dropzone was not expected"


def assert_label(compo, label_text, label_for, label_col=None):
    compo_html = etree.fromstring(compo.render())
    label = compo_html.find(".//label")
    assert label is not None, "label not found"
    assert label.text == label_text, "label text not correct"
    assert label.attrib.get("for", None) == label_for, "label for not correct"
    assert "control-label" in label.attrib.get("class", None), "label class control-label missing"
    if label_col is not None:
        assert "col-sm-%s" % label_col in label.attrib.get("class", None), "label_col class not correct"


def assert_no_label(compo):
    compo_html = etree.fromstring(compo.render())
    label = compo_html.find(".//label")
    assert label is None, "label found bot no label was expeted"


def assert_image(compo, src):
    compo_html = etree.fromstring(compo.render())
    image = compo_html.find(".//img")
    assert image is not None, "could not find preview image"
    assert image.attrib.get("src", None) == src, "wrong src"
    assert "epfl-upload-image" in image.attrib.get("class", None), "wrong class"


def assert_no_image(compo):
    compo_html = etree.fromstring(compo.render())
    image = compo_html.find(".//img")
    assert image is None, "find preview image but no image is expceted"


def assert_remove_icon(compo):
    compo_html = etree.fromstring(compo.render())
    remove_icon = compo_html.find(".//i[@class='fa fa-times fa-lg color-danger epfl-upload-remove-icon']")
    assert remove_icon is not None, "could not find remove icon"


def assert_no_remove_icon(compo):
    compo_html = etree.fromstring(compo.render())
    remove_icon = compo_html.find(".//i[@class='fa fa-times fa-lg color-danger epfl-upload-remove-icon']")
    assert remove_icon is None, "found remove icon but no one was expected"


# Tests
###############################################################################

def test_no_options(page):
    page.root_node = components.Upload()
    page.handle_transaction()

    compo = page.root_node

    assert_outer_div(compo)
    assert_file_input(compo)
    assert_no_label(compo)
    assert_no_dropzone(compo)


def test_simple_options(page):
    page.root_node = components.Upload(
        name="test_upload",
        label="test_upload_label",
        height="250",
        width="250",
        mandatory=True,
        label_col=4,
    )
    page.handle_transaction()

    compo = page.root_node
    assert_outer_div(compo, height="250", width="250", mandatory=True)
    assert_file_input(compo, name="test_upload")
    assert_no_dropzone(compo)
    assert_label(compo, label_text="test_upload_label", label_for="root_node_input", label_col=4)


def test_validation_error(page):
    page.root_node = components.Upload(
        name="test_upload",
        label="test_upload_label",
        height="250",
        width="250",
        mandatory=True,
        validation_error="AAHHH SOMETHING IS WRONG !!!"
    )
    page.handle_transaction()

    compo = page.root_node
    assert_outer_div(compo, height="250", width="250", mandatory=True)
    assert_file_input(compo, name="test_upload")
    assert_no_dropzone(compo)
    assert_label(compo, label_text="test_upload_label", label_for="root_node_input")

    compo_html = etree.fromstring(compo.render())
    error_div = compo_html.find("div")
    assert "has-error" in error_div.attrib.get("class", None), "error class not set correct"

    error_text = compo_html.find(".//small")
    assert error_text.text == "AAHHH SOMETHING IS WRONG !!!", "error text is not correct"
    assert "help-block" in error_text.get("class", None), "wrong class in error text"


def test_layout_vertical(page):
    page.root_node = components.Upload(
        name="test_upload",
        label="test_upload_label",
        height="250",
        width="250",
        mandatory=True,
        layout_vertical=True,
    )
    page.handle_transaction()

    compo = page.root_node
    assert_outer_div(compo, height="250", width="250", mandatory=True)
    assert_file_input(compo, name="test_upload")
    assert_no_dropzone(compo)
    assert_label(compo, label_text="test_upload_label", label_for="root_node_input")

    compo_html = etree.fromstring(compo.render())
    row_divs = compo_html.findall("div[@class='row']")
    assert len(row_divs) == 2, "not all row divs found in layout vertical"

    for row_div in row_divs:
        cols = row_div.findall("div")
        assert len(cols) == 1, "not all row divs have correct col divs"
        assert "col-sm-12" in cols[0].attrib.get("class", None), "col divs wrong size"


def test_dropzone_simple(page):
    page.root_node = components.Upload(
        name="test_upload",
        label="test_upload_label",
        height="250",
        width="250",
        show_drop_zone=True
    )
    page.handle_transaction()

    compo = page.root_node

    assert_outer_div(compo, height="250", width="250")
    assert_file_input(compo)
    assert_dropzone(compo)
    assert_label(compo, label_text="test_upload_label", label_for="root_node_input")


def test_dropzone_simple_with_no_file_input(page):
    page.root_node = components.Upload(
        name="test_upload",
        label="test_upload_label",
        height="250",
        width="250",
        show_drop_zone=True,
        show_file_upload_input=False
    )
    page.handle_transaction()

    compo = page.root_node

    assert_outer_div(compo, height="250", width="250")
    assert_no_file_input(compo)
    assert_dropzone(compo)
    assert_label(compo, label_text="test_upload_label", label_for="root_node_input")


def test_dropzone_with_options(page):
    page.root_node = components.Upload(
        name="test_upload",
        label="test_upload_label",
        height="250",
        width="250",
        show_drop_zone=True,
        plus_icon_size="lg",
        drop_zone_add_text="drop zone test text",
        drop_zone_add_position_top="1337"
    )
    page.handle_transaction()

    compo = page.root_node

    assert_outer_div(compo, height="250", width="250")
    assert_file_input(compo, name="test_upload")
    assert_dropzone(compo, drop_zone_add_position_top="1337", drop_zone_add_text="drop zone test text")
    assert_label(compo, label_text="test_upload_label", label_for="root_node_input")


def test_change_dropzone_fileinput_no_preview(page):
    page.root_node = components.Upload(
        name="test_upload",
        label="test_upload_label",
        height="250",
        width="250",
        show_drop_zone=True,
        no_preview=True
    )
    page.handle_transaction()

    compo = page.root_node

    assert_outer_div(compo, height="250", width="250")
    assert_file_input(compo, name="test_upload")
    assert_dropzone(compo)
    assert_label(compo, label_text="test_upload_label", label_for="root_node_input")

    compo.handle_change(IMAGE_BASE_64_BROWSER)
    compo.render_cache = None

    assert_no_image(compo)
    assert compo.get_value() == IMAGE_BASE_64_BROWSER, "Wrong Value"
    assert base64.b64encode(compo.get_as_binary()) == IMAGE_BASE_64_SERVER, "get as binary wrong result"

    # assert_remove_icon(compo)

    compo.handle_remove_icon()
    compo.render_cache = None

    assert compo.get_value() == None, "value not correct reseted"
    assert compo.get_as_binary() == None, "get as binary not correct reseted"


def test_change_dropzone_fileinput(page):
    page.root_node = components.Upload(
        name="test_upload",
        label="test_upload_label",
        height="250",
        width="250",
        show_drop_zone=True
    )
    page.handle_transaction()

    compo = page.root_node

    assert_outer_div(compo, height="250", width="250")
    assert_file_input(compo, name="test_upload")
    assert_dropzone(compo)
    assert_label(compo, label_text="test_upload_label", label_for="root_node_input")

    compo.handle_change(IMAGE_BASE_64_BROWSER)
    compo.render_cache = None

    assert_image(compo, src=IMAGE_BASE_64_BROWSER)
    assert compo.get_value() == IMAGE_BASE_64_BROWSER, "Wrong Value"
    assert base64.b64encode(compo.get_as_binary()) == IMAGE_BASE_64_SERVER, "get as binary wrong result"

    assert_remove_icon(compo)

    compo.handle_remove_icon()
    compo.render_cache = None

    assert_no_remove_icon(compo)
    assert_no_image(compo)

    assert compo.get_value() == None, "value not correct reseted"
    assert compo.get_as_binary() == None, "get as binary not correct reseted"
