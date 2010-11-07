# -*- coding: utf-8 -*-
## Copyright (c) 2009-2010 elij
##
## Permission is hereby granted, free of charge, to any person obtaining a copy
## of this software and associated documentation files (the "Software"), to deal
## in the Software without restriction, including without limitation the rights
## to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
## copies of the Software, and to permit persons to whom the Software is
## furnished to do so, subject to the following conditions:
##
## The above copyright notice and this permission notice shall be included in
## all copies or substantial portions of the Software.
##
## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
## IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
## FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
## AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
## LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
## OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
## THE SOFTWARE.
##
from ctypes import *
from ctypes.util import find_library
import sys
import os
import exceptions

class CronkiteException(Exception):
    pass

class CKPackage(Structure):
    pass

CKPackage._fields_ = [("values", c_char_p * 10), ("next", POINTER(CKPackage))]

libname = find_library("cronkite")
if libname == None:
    ## just guess. seems old version of python/ctypes on linux fail for this
    libname = 'libcronkite.so'

_libcronkite = cdll.LoadLibrary(libname)
_libcronkite.cronkite_setopt.argtypes = [c_int, c_char_p]
_libcronkite.cronkite_setopt.restype = c_void_p
_libcronkite.cronkite_get.argtypes = [c_char, c_char_p]
_libcronkite.cronkite_get.restype = POINTER(CKPackage)
_libcronkite.cronkite_cleanup.argtypes = [POINTER(CKPackage)]
_libcronkite.cronkite_cleanup.restype = c_void_p
_libcronkite.cronkite_strerror.argtypes = [c_int]
_libcronkite.cronkite_strerror.restype = c_char_p
ck_errno = c_int.in_dll(_libcronkite, "ck_errno")

# manually define the enum for ck_options
CK_OPT_AURURL = 0
CK_OPT_HTTP_PROXY = 1

def q_unpack(cpkg):
    return {"id":          cpkg.contents.values[0],
            "url":         cpkg.contents.values[1],
            "name":        cpkg.contents.values[2],
            "version":     cpkg.contents.values[3],
            "urlpath":     cpkg.contents.values[4],
            "license":     cpkg.contents.values[5],
            "numvotes":    cpkg.contents.values[6],
            "outofdate":   cpkg.contents.values[7],
            "categoryid":  cpkg.contents.values[8],
            "description": cpkg.contents.values[9]}

def setopt(opt, val):
    optUC = opt.upper()
    if (optUC == 'AURURL'):
        _libcronkite.cronkite_setopt(CK_OPT_AURURL, val);
    elif (optUC == 'HTTP_PROXY'):
        _libcronkite.cronkite_setopt(CK_OPT_HTTP_PROXY, val);
    else:
        raise exceptions.TypeError("Bad option")

def query(qtype, qstring):
    if not qtype == 's' and not qtype == 'i' and not qtype == 'm':
        raise exceptions.TypeError("argument 1 must be 'i', 's', or 'm'")
        return
    results = []
    pkg = _libcronkite.cronkite_get(qtype, qstring)
    if bool(pkg) == False:
        # save errno because cleanup resets it
        err = ck_errno.value
        # do some cleanup
        _libcronkite.cronkite_cleanup(pkg)
        # if err!=0, something broke
        # otherwise just empty results -- no results found
        if err != 0:
            raise CronkiteException(_libcronkite.cronkite_strerror(err))
    else:
        results.append(q_unpack(pkg))
        next = pkg.contents.next
        while next:
            results.append(q_unpack(next))
            next = next.contents.next
    _libcronkite.cronkite_cleanup(pkg)
    return results
