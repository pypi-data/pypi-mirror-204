
'''
Nuitka BuildTarget

Copyright (c) 2015 - 2022 Rob "N3X15" Nelson <nexisentertainment@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import datetime
import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from nuitka.plugins import Plugins as NuitkaPlugins
from nuitka.plugins.PluginBase import NuitkaPluginBase

from buildtools.bt_logging import IndentLogger

from .. import os_utils
from .base_target import SingleBuildTarget

log = IndentLogger(logging.getLogger(__name__))

DEBUG: bool = False


class NuitkaTarget(SingleBuildTarget):
    BT_LABEL = 'NUITKA'

    _CACHED_ALWAYS_ENABLED_PLUGINS: Optional[Set[str]] = None

    def __init__(self, entry_point: Union[str, Path], package_name: str, files: List[Union[str, Path]], dependencies: List[Union[str, Path]] = [], tmp_dir: Optional[Union[str, Path]] = None, single_file: bool = True, nuitka_subdir: Optional[Union[str, Path]] = None) -> None:
        if tmp_dir is None:
            tmp_dir = Path('.tmp')
        else:
            tmp_dir = Path(tmp_dir)
        self.python_path = sys.executable
        self.entry_point: Path = Path(entry_point)
        self.package_name: str = package_name
        self.out_dir: Path = tmp_dir / 'nuitka'
        if nuitka_subdir:
            self.out_dir = self.out_dir / nuitka_subdir
        self.dist_dir: Path = self.out_dir / f'{self.package_name}.dist'
        self.singlefile: bool = single_file
        self.executable_mangled: Path = self.dist_dir / self.package_name if not single_file else (self.out_dir / self.package_name).with_suffix('.bin')

        if os.name == 'nt':
            self.executable_mangled = self.executable_mangled.with_suffix('.exe')

        self.windows_disable_console: bool = False
        #: See Nuitka --windows-icon-from-ico for format
        self.windows_icon_from_ico: List[Union[str, Path]] = []
        self.windows_icon_from_exe: Optional[Union[str, Path]] = None
        self.windows_onefile_splash_image: Optional[Union[str, Path]] = None
        self.windows_uac_admin: bool = False
        self.windows_uac_uiaccess: bool = False
        self.product_name: str = 'Nuitka Executable'
        self.company_name: str = 'Nuitka Executable Contributors'
        self.file_version: Tuple[int, int, int, int] = (0, 0, 0, 0)
        self.product_version: Tuple[int, int, int, int] = (0, 0, 0, 0)
        self.file_description: str = 'FIXME: Review target.product_name, target.company_name, target.file_version, target.trademarks, and target.file_description.'
        self.trademarks: str = f'FIXME: Copyright ©{datetime.datetime.now().year} Company Name Here. All Rights Reserved.'

        self.linux_onefile_icon: Optional[Union[str, Path]] = None

        super().__init__(target=str(self.executable_mangled), files=list(map(str, files)), dependencies=list(map(str, dependencies)))

        self.included_packages: Set[str] = set()
        self.included_modules: Set[str] = set()
        self.included_plugin_directories: Set[Path] = set()
        self.included_plugin_files: Set[str] = set()
        self.enabled_plugins: Set[str] = set()
        self._always_active_plugins: Set[str] = set()
        self._always_active_plugins = self.getAlwaysActivePluginNames()
        self.nofollow_imports: bool = False
        self.follow_import_to: List[str] = []
        self.nofollow_import_to: List[str] = []
        self.pgo: bool = False
        self.lto: bool = False
        self.python_flags: str=''
        self.onefile_tempdir_spec: Optional[str] = None

    def get_config(self) -> Dict[str, Any]:
        return super().get_config()

    def getAlwaysActivePluginNames(self) -> Set[str]:
        if self._CACHED_ALWAYS_ENABLED_PLUGINS is None:
            log.debug(f'_CACHED_ALWAYS_ENABLED_PLUGINS is None, calculating...')
            self._CACHED_ALWAYS_ENABLED_PLUGINS = set()
            try:
                NuitkaPlugins.loadPlugins()
                # print(repr(NuitkaPlugins.getActivePlugins()))
                for plugin_name in sorted(NuitkaPlugins.plugin_name2plugin_classes):
                    plugin: NuitkaPluginBase = NuitkaPlugins.plugin_name2plugin_classes[plugin_name][0]
                    if plugin.isAlwaysEnabled():
                        self._CACHED_ALWAYS_ENABLED_PLUGINS.add(plugin.plugin_name)
            except Exception as e:
                log.critical('Error interfacing with Nuitka:')
                log.critical(e)
            log.debug(f'_CACHED_ALWAYS_ENABLED_PLUGINS = {self._CACHED_ALWAYS_ENABLED_PLUGINS!r}')
        return self._CACHED_ALWAYS_ENABLED_PLUGINS

    def build(self):
        opts: List[str] = [
            '--prefer-source-code',
            '--assume-yes-for-downloads',
            # '--recurse-all',
            # '--follow-imports',
        ]
        if os.name != 'nt':
            opts.append('--static-libpython=yes')
        if self.nofollow_imports:
            opts.append('--nofollow-imports')
        if len(self.follow_import_to)>0:
            # opts.append(f'--follow-import-to='+(','.join(self.recurse_to)))
            opts += [f'--follow-import-to={x}' for x in self.follow_import_to]
        if len(self.nofollow_import_to)>0:
            # opts.append(f'--follow-import-to='+(','.join(self.recurse_to)))
            opts += [f'--nofollow-import-to={x}' for x in self.nofollow_import_to]
        for pkg in sorted(self.included_packages):
            opts.append(f'--include-package={pkg}')
        for pkg in sorted(self.included_modules):
            opts.append(f'--include-module={pkg}')
        for pd in sorted(self.included_plugin_directories):
            opts.append(f'--include-plugin-directory={pd}')
        for pf in sorted(self.included_plugin_files):
            opts.append(f'--include-plugin-files={pf}')
        # print('ENABLED', repr(self.enabled_plugins))
        # print('ALWAYS', repr(self._always_active_plugins))
        for plug in sorted(self.enabled_plugins - self._always_active_plugins):
            opts.append(f'--enable-plugin={plug}')
        if self.lto:
            opts.append('--lto=yes')
        if self.pgo:
            opts.append('--pgo')
        if len(self.python_flags)>0:
            opts.append('--python-flags='+self.python_flags)
        opts += [
            f'--output-dir={self.out_dir}',
            # '--show-progress', # *screaming*
            '--standalone'
        ]
        if self.singlefile:
            opts += ['--onefile']
            if self.onefile_tempdir_spec is not None:
                opts.append(f'--onefile-tempdir-spec={self.onefile_tempdir_spec}')
            if os_utils.is_linux():
                if self.linux_onefile_icon is not None:
                    opts.append(
                        f'--linux-onefile-icon={self.linux_onefile_icon}')
            if os_utils.is_windows():
                if self.windows_onefile_splash_image is not None:
                    opts.append(
                        f'--onefile-windows-splash-screen-image={self.windows_onefile_splash_image}')

        if os_utils.is_windows():
            if self.windows_disable_console:
                opts.append('--windows-disable-console')
            if self.windows_icon_from_exe:
                opts.append(
                    f'--windows-icon-from-exe={self.windows_icon_from_exe}')
            if len(self.windows_icon_from_ico) > 0:
                for ico_spec in self.windows_icon_from_ico:
                    opts.append(f'--windows-icon-from-ico={ico_spec}')
            if self.windows_uac_admin:
                opts.append('--windows-uac-admin')
            if self.windows_uac_uiaccess:
                opts.append('--windows-uac-uiaccess')
        opts += [
            f'--product-name={self.product_name}',
            f'--product-version=' +
            ('.'.join(map(str, self.product_version))),
            f'--company-name={self.company_name}',
            f'--file-version=' +
            ('.'.join(map(str, self.file_version))),
            f'--file-description={self.file_description}',
            f'--trademarks={self.trademarks}',
        ]
        nuitka_cmd: List[str] = [str(sys.executable), '-m', 'nuitka']
        nuitka_cmd += opts
        nuitka_cmd.append(str(self.entry_point))
        os_utils.cmd(nuitka_cmd, echo=True, show_output=True, critical=True, globbify=False)
