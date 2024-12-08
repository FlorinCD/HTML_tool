import logging
import os
import pytest

from ..common.path import Path

@pytest.mark.unit
def test_relative_path():
    path = "/dir0/dir1/file_to_get"
    base_path = "/dir2/dir3/"  # ../../dir0/dir1/file_to_get

    path_obj = Path(path)
    assert path_obj.relative_path(base_path) == os.path.relpath(path, base_path)

@pytest.mark.unit
def test_is_absolute_path():
    path = r"C:\Users\Florin\PycharmProjects\HTML_tool\HTML_tool"
    path_obj = Path(path)
    assert path_obj.is_absolute()

@pytest.mark.unit
def test_join():
    path = "dir0\\dir1"
    path_obj = Path(path)
    assert path_obj.join("dir2\\file0").path == Path("dir0\\dir1\\dir2\\file0").path

@pytest.mark.unit
def test_repr_():
    path = "dir0\\file3"
    path_obj = Path(path)
    assert path_obj.__repr__() == "Path(dir0\\file3)"

@pytest.mark.unit
def test_dirname():
    path = "C:\\Users\\Florin\\Something\\Directory\\File.txt"
    obj_path = Path(path)
    assert obj_path.dirname() == "C:\\Users\\Florin\\Something\\Directory"

@pytest.mark.unit
def test_path_exists():
    path = os.getcwd()
    obj_path = Path(path)
    assert obj_path.exists()

@pytest.mark.unit
def test_path_is_file():
    path = "C:\\Users\\Florin\\PycharmProjects\\HTML_tool\\HTML_tool\\README.md"
    obj_path = Path(path)
    assert obj_path.is_file()

@pytest.mark.unit
def test_path_is_dir():
    path = "C:\\Users\\Florin\\PycharmProjects\\HTML_tool\\HTML_tool"
    obj_path = Path(path)
    assert obj_path.is_dir()

@pytest.mark.unit
def test_to_absolute_path():
    relative_path = "README.md"
    absolute_path = "C:\\Users\\Florin\\PycharmProjects\\HTML_tool\\HTML_tool\\README.md"
    obj_path = Path(relative_path)
    logging.error(obj_path.absolute_path)
    assert obj_path.absolute_path == absolute_path

@pytest.mark.unit
def test_local_reference():
    local_reference = "./dir0/file.txt"
    outside_reference = "https://www.youtube.com"
    assert Path.is_local_reference(local_reference)
    assert not Path.is_local_reference(outside_reference)