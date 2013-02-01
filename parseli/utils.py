#!/usr/bin/env python
#-*- coding: utf-8

"""
    parseli.utils
    ~~~~~~~~~~~~~
    Utilities taken from various sources, including web.py

    :copyright: (c) 2012 by Aaron Swartz <me@aaronsw.com>, Anand Chitipothu <anandology@gmail.com>
    :license: See web.py license - https://github.com/webpy/webpy/blob/master/LICENSE.txt
"""

__all__ = ["Storage"]

class Storage(dict):
    """
    A Storage object is like a dictionary except `obj.foo` can be used
    in addition to `obj['foo']`.
    
        >>> o = storage(a=1)
        >>> o.a
        1
        >>> o['a']
        1
        >>> o.a = 2
        >>> o['a']
        2
        >>> del o.a
        >>> o.a
        Traceback (most recent call last):
            ...
        AttributeError: 'a'
    
    """
    def __getattr__(self, key): 
        try:
            return self[key]
        except KeyError, k:
            raise AttributeError, k
    
    def __setattr__(self, key, value): 
        self[key] = value
    
    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError, k:
            raise AttributeError, k
    
    def __repr__(self):     
        return '<Storage ' + dict.__repr__(self) + '>'

