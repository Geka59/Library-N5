from unittest import TestCase, mock
from unittest.mock import patch
import pytest
from user_interface import UserInterface


class UITest(TestCase):
    def test_out_table(self):
        uik = UserInterface()
        uik.out_table([['2', 'Как вывести октавию на сверхвук ', 'Б.Р. Штольц\n','gdf','Евгк','23.566','45.67']])