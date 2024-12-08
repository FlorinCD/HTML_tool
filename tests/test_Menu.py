import logging
import pytest

from ..common.menu import Menu, ReadMe

@pytest.mark.unit
def test_decorate_menu():
    obj_menu = Menu()
    obj_menu.decorate_menu()

@pytest.mark.unit
def test_read_me():
    obj_menu = ReadMe()