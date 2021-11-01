#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Is it markdown?
"""

import logging
import regex as re
logger = logging.getLogger(__name__)


class MarkdownDetector:

    def __init__(self):
        self.patterns = [
            r'#+\s+.+',
            r'=+',
            r'-+',
            r'>\s+.+',
            r'\s*[*+-]\s+.+',
            r'\s*\d+\.\s+.+',
            r'<.+',
            r'\[.+',
            r'(\*|\*\*|_|__).+',
            r'\\.+',
            r'`.+',
            r'!\[.+',
            r'[\p{Letter}"%\.\()][\p{Letter}\p{Mark}\p{Separator}\p{Symbol}\p{Number}\p{Punctuation}]+'
        ]
        for p in self.patterns:
            re.compile(f'^{p}$')
        self.rxx = [re.compile(f'^{p}$') for p in self.patterns]

    def detect(self, s: str):
        if not isinstance(s, str):
            raise TypeError(f'Expected {str}, got {type(s)}.')
        lines = [l.strip() for l in s.split('\n') if l.strip() != '']
        hits = 0
        for line in lines:
            for i, rx in enumerate(self.rxx):
                m = rx.match(line)
                if m is not None:
                    hits += 1
                    break
        return float(hits) / float(len(lines))

