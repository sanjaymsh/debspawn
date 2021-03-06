# -*- coding: utf-8 -*-
#
# Copyright (C) 2018-2020 Matthias Klumpp <matthias@tenstral.net>
#
# Licensed under the GNU Lesser General Public License Version 3
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the license, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import json


thisfile = __file__
if not os.path.isabs(thisfile):
    thisfile = os.path.normpath(os.path.join(os.getcwd(), thisfile))


__all__ = ['GlobalConfig']


class GlobalConfig:
    '''
    Global configuration singleton affecting all of Debspawn.
    '''

    _instance = None

    class __GlobalConfig:
        def load(self, fname=None):
            if not fname:
                fname = '/etc/debspawn/global.json'

            jdata = {}
            if os.path.isfile(fname):
                with open(fname) as json_file:
                    try:
                        jdata = json.load(json_file)
                    except json.JSONDecodeError as e:
                        print('Unable to parse global configuration (global.json): {}'.format(str(e)), file=sys.stderr)
                        sys.exit(8)

            self._dsrun_path = os.path.normpath(os.path.join(thisfile, '..', 'dsrun'))
            if not os.path.isfile(self._dsrun_path):
                print('Debspawn is not set up properly: Unable to find file "{}". Can not continue.'.format(self._dsrun_path), file=sys.stderr)
                sys.exit(4)

            self._osroots_dir = jdata.get('OSRootsDir', '/var/lib/debspawn/containers/')
            self._results_dir = jdata.get('ResultsDir', '/var/lib/debspawn/results/')
            self._aptcache_dir = jdata.get('APTCacheDir', '/var/lib/debspawn/aptcache/')
            self._injected_pkgs_dir = jdata.get('InjectedPkgsDir', '/var/lib/debspawn/injected-pkgs/')
            self._temp_dir = jdata.get('TempDir', '/var/tmp/debspawn/')
            self._allow_unsafe_perms = jdata.get('AllowUnsafePermissions', False)

        @property
        def dsrun_path(self) -> str:
            return self._dsrun_path

        @dsrun_path.setter
        def dsrun_path(self, v) -> str:
            self._dsrun_path = v

        @property
        def osroots_dir(self) -> str:
            return self._osroots_dir

        @property
        def results_dir(self) -> str:
            return self._results_dir

        @property
        def aptcache_dir(self) -> str:
            return self._aptcache_dir

        @property
        def injected_pkgs_dir(self) -> str:
            return self._injected_pkgs_dir

        @property
        def temp_dir(self) -> str:
            return self._temp_dir

        @property
        def allow_unsafe_perms(self) -> bool:
            return self._allow_unsafe_perms

    def __init__(self, fname=None):
        if not GlobalConfig._instance:
            GlobalConfig._instance = GlobalConfig.__GlobalConfig()
            GlobalConfig._instance.load(fname)

    def __getattr__(self, name):
        return getattr(self._instance, name)
