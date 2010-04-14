# -*- coding: utf-8 -*-
##
## Copyright 2009 elij
##
## Licensed under the Apache License, Version 2.0 (the "License"); you may
## not use this file except in compliance with the License. You may obtain
## a copy of the License at
##
## http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
## WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
## License for the specific language governing permissions and limitations
## under the License.
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
_libcronkite.cronkite_seturl.argtypes = [c_char_p]
_libcronkite.cronkite_seturl.restype = c_void_p
_libcronkite.cronkite_get.argtypes = [c_char, c_char_p]
_libcronkite.cronkite_get.restype = POINTER(CKPackage)
_libcronkite.cronkite_cleanup.argtypes = [POINTER(CKPackage)]
_libcronkite.cronkite_cleanup.restype = c_void_p
_libcronkite.cronkite_strerror.argtypes = [c_int]
_libcronkite.cronkite_strerror.restype = c_char_p
ck_errno = c_int.in_dll(_libcronkite, "ck_errno")

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

def seturl(newurl):
    _libcronkite.cronkite_seturl(newurl);

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
