##    Threadsnake. A tiny experimental server-side express-like library.
##    Copyright (C) 2022  Erick Fernando Mora Ramirez
##
##    This program is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    This program is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with this program.  If not, see <https://www.gnu.org/licenses/>.
##
##    mailto:erickfernandomoraramirez@gmail.com

import importlib
import importlib.util
import os
import socket
import sys
from types import ModuleType
from typing import List, Tuple
from uuid import uuid4
import __main__

from ..application import Application
from ..router import Router

ConfiguredRoute = Tuple[str, List[Router]]

def import_module(path:str) -> ModuleType:
    if not path.endswith('.py'):
        path += '.py'    
    moduleName:str = os.path.basename(path) + str(uuid4()).replace('-', '')
    spec = importlib.util.spec_from_file_location(moduleName, path)
    module:ModuleType = importlib.util.module_from_spec(spec)
    sys.modules[moduleName] = module
    spec.loader.exec_module(module)
    return module

def routes_to(app:Application, path:str, root:str):
    baseFolder:str = os.path.dirname(__main__.__file__)
    fullSearchPath = os.sep.join([baseFolder, path.replace('/', os.sep)])
    module:ModuleType = import_module(fullSearchPath)
    for property in dir(module):
        router = getattr(module, property)
        if isinstance(router, Router):
            app.use_router(router, root)

def routes_to_folder(app:Application, path:str):
    location:str = os.path.dirname(os.path.abspath(__main__.__file__))
    fullSearchPath = os.sep.join([location, path])
    fullSearchPath = fullSearchPath.replace('/', os.sep).replace('\\', os.sep)
    files = [
        [path, result[0][len(fullSearchPath)+1:].replace('\\', '/'), file[:-3]] 
        for result in os.walk(fullSearchPath) for file in result[2]
        if file.endswith('.py')
    ]
    routes = [
        [
            '/'.join([j for j in i if len(j) > 0]),
            '/'.join([j for j in i[1:] if len(j) > 0])
        ]
        for i in files
    ]
    for route in routes:
        path, root = route
        routes_to(app, path, root)

def get_next_free_port(start:int = 8080):
    while start < 65535:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("", start))
                return start
            except OSError:
                start += 1