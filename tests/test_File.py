import logging
import pytest

from ..common.files import File, HtmlFile, LogFile, LoggerHTML
from ..common.path import Path

@pytest.fixture
def setup_html_file_fixture():
    path = "test_files/html_for_test.html"
    html_file = HtmlFile(path)
    logging.error(html_file.file_path)
    return html_file

@pytest.mark.unit
def test_file_read_file(setup_html_file_fixture):
    content = setup_html_file_fixture.read_file()
    bad_content = HtmlFile("this/path/doesn't/exist/file.html").read_file()
    assert "<html" in content
    assert bad_content == ""

@pytest.mark.unit
def test_file_file_name(setup_html_file_fixture):
    assert setup_html_file_fixture.file_name == "test_files/html_for_test.html".split('\\')[-1]

@pytest.mark.unit
def test_file_add_reference(setup_html_file_fixture):
    setup_html_file_fixture.add_reference("External Link","https://","is_absolute")
    length = len(setup_html_file_fixture.references)
    assert length == 1

@pytest.mark.unit
def test_html_file_exists(setup_html_file_fixture):
    assert setup_html_file_fixture.file_path.exists()

@pytest.mark.unit
def test_file_is_html(setup_html_file_fixture):
    assert HtmlFile.is_html_file("../test_files/html_for_test.html")

@pytest.mark.unit
def test_modify_local_references():
    path = "test_files/html_for_test.html"
    html_file = HtmlFile(path, True, True, True)
    html_file.modify_local_references()