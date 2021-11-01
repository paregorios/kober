#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File format decipherer
"""

from kober.markdown import MarkdownDetector
import logging
import magic
import mimetypes
from pathlib import Path


logger = logging.getLogger(__name__)

class Decipherer:

    def __init__(self, modes=['mimetypes_guess_type', 'magic_from_file']):
        mimetypes.init()
        mimetypes.add_type('text/markdown', '.markdown', strict=True)  # RFC 7763 The text/markdown Media Type
        mimetypes.add_type('text/markdown', '.md', strict=True)  # RFC 7763 The text/markdown Media Type
        self.modes = modes
        self.criteria = {
            'magic_from_file': {
                'success': 'debug',
                'failure': 'warn'
            },
            'mimetypes_guess_type': {
                'success': 'debug',
                'failure': 'warn'
            }
        }

    def decipher(self, filepath):
        logger.debug(f'filepath: "{filepath}"')
        if isinstance(filepath, Path):
            inpath = filepath
        elif isinstance(filepath, str):
            inpath = Path(filepath)
        inpath = inpath.expanduser().resolve()
        logger.debug(f'inpath: "{inpath}"')

        mime_types = dict()
        encodings = dict()
        attempts = 0
        for k, criterion in self.criteria.items():
            if k in self.modes:
                attempts += 1
                mime, encoding, raw_score = getattr(self, f'_try_{k}')(inpath, criterion)
                if mime is not None:
                    try:
                        mime_types[mime]
                    except KeyError:
                        mime_types[mime] = 0.0
                    finally:
                        mime_types[mime] += raw_score
                if encoding is not None:
                    try:
                        encodings[encoding]
                    except KeyError:
                        encodings[encoding] = 0.0
                    finally:
                        encodings[encoding] += raw_score
        attempts = float(attempts)
        for mime, score in mime_types.items():
            mime_types[mime] = score / attempts
        try:
            mime_types['text/plain']
        except KeyError:
            pass
        else:
            mime_types['text/markdown'] = self._try_markdown(inpath)
        for encoding, score in encodings.items():
            encodings[encoding] = score / attempts
        return mime_types, encodings

    def _try_markdown(self, inpath: Path):
        try:
            getattr(self, 'markdown_detector')
        except AttributeError:
            self.markdown_detector = MarkdownDetector()
        with open(inpath, 'r') as f:
            md = f.read()
        del f
        return self.markdown_detector.detect(md)

    def _try_magic_from_file(self, inpath: Path, criterion: dict):
        score = 0.0
        magician = magic.Magic(mime=True, mime_encoding=True, uncompress=True)
        spell = magician.from_file(str(inpath))
        mime, encoding = [p.strip() for p in spell.split(';')]
        if mime is None:
            response = criterion['failure']
            getattr(logger, response)(f'magic.from_file() failed on file "{inpath}".')
        else:
            response = criterion['success']
            getattr(logger, response)(f'magic.from_file() succeeded on file "{inpath}" = {mime}')
            score = 1.0
        return mime, encoding, score

    def _try_mimetypes_guess_type(self, inpath: Path, criterion: dict):
        score = 0.0
        mime, encoding = mimetypes.guess_type(inpath, strict=False)
        if mime is None:
            response = criterion['failure']
            getattr(logger, response)(f'mimetypes.guess_type() failed on file "{inpath}".')
        else:
            response = criterion['success']
            getattr(logger, response)(f'mimetypes.guess_type() succeeded on file "{inpath}" = {mime}')
            score = 1.0
        return mime, encoding, score

        


