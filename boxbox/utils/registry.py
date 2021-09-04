import re
import pandas as pd

from copy import deepcopy
from functools import partial
from collections.abc import Iterable
from typing import Dict, List, Any


class Registrar:

    def __init__(self,
                 name: str,
                 options: Dict[str, List[str]] = None,
                 hook_on: bool = False):
        _pattern = '(?<base_name>.*)'
        if options is not None:
            for k, v in options.items():
                assert isinstance(v, Iterable) and len(v) > 1, \
                        'All options should be Iterable and more than one.'
                for option in v:
                    assert isinstance(option, str), 'Only support str option.'

                _pattern += '_(' + '<?' + k + '>' + '|'.join(v) + ')'
        self._pattern = repr(_pattern)[1:-1]
        self._options = deepcopy(options)

        self._name = name
        self.enable
        self._module_dict = dict()
        self._data_frame = pd.DataFrame(columns=options.keys())

    @property
    def name(self):
        return self._name
    
    def __repr__(self):
        return self.__class__.__name__ + \
                f'(name={self._name}, ' + \
                f'_options={self._options}, ' + \
                f'_module_dict={self._module_dict})'

    def _register(self, module: Any, force: bool = False):
        full_name = module.__name__
        match_objs = re.match(self._pattern, full_name)
        if match_objs is None:
            raise ValueError(f'The module name cannot match the pattern of {self._name}')

        if full_name not in self._module_dict:
            module_infos = dict(full_name=full_name, base_name=match_objs.group('base_name'))
            for k in self._options.keys():
                module_infos[k] = match_objs.group(k)
            self._data_frame.append(module_infos, ignore_index=True)

        if force or (full_name not in self._module_dict):
            self._module_dict[full_name] = module
        else:
            raise ValueError(f'The module {module} has been registerred.')

        if self.hook_flag:
            self.after_register_hook(full_name)

    def register_module(self, force: bool = False, module: Any = None):
        if module is not None:
            self._register(module, force=force)
        
        register_func = partial(self._register, force=force)
        return register_func
    
    def enable_hook(self):
        self.hook_flag = True