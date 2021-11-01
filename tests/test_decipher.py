#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test decipher module"""

import logging
from nose.tools import assert_equal, assert_false, assert_true, raises
from kober.decipher import Decipherer
from pathlib import Path
from pprint import pprint
from unittest import TestCase

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
test_data_path = Path('tests/data').resolve()


def setup_module():
    """Change me"""
    pass


def teardown_module():
    """Change me"""
    pass


class Test_Markdown(TestCase):

    def setUp(self):
        self.files = list()
        context = test_data_path / 'markdown'
        self.filepaths = list()
        for fn in ['daringfireball']:
            for suffix in ['', '.md', '.markdown', '.text', '.txt']:
                fp = context / f'{fn}{suffix}'
                self.filepaths.append(fp)

    def test_mimetypes_guess_type(self):
        d = Decipherer(modes=['mimetypes_guess_type'])
        expected_mime_types = {
            '': list(),
            '.md': ['text/markdown'],
            '.markdown': ['text/markdown'],
            '.text': ['text/plain'],
            '.txt': ['text/plain']
        }
        for fp in self.filepaths:
            mime_types, encodings = d.decipher(fp)
            s = fp.suffix
            for expected in expected_mime_types[s]:
                assert_true(expected in list(mime_types.keys()))
            for encoding in encodings:
                assert_equal(0, len(encoding))
            
    def test_magic_from_file(self):
        d = Decipherer(modes=['magic_from_file'])
        expected_mime_types = {
            '': ['text/plain'],
            '.md': ['text/plain'],  # yep, magic doesn't do anything for you on markdown
            '.markdown': ['text/plain'],
            '.text': ['text/plain'],
            '.txt': ['text/plain']
        }
        for fp in self.filepaths:
            mime_types, encodings = d.decipher(fp)
            s = fp.suffix
            print(f'mime_types: {list(mime_types.keys())}')
            for expected in expected_mime_types[s]:
                print(f'expected: {expected}')
                assert_true(expected in list(mime_types.keys()))
            #for encoding in encodings:
            #    assert_equal(0, len(encoding))

