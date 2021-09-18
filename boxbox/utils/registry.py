import re
import uuid
import pandas as pd

from copy import deepcopy
from functools import partial
from typing import Dict, List, Any
from collections.abc import Iterable


class Registrar:

    def __init__(self, name: str, options: Dict[str, List[str]] = None):
        options = {} if options is None else options
        _pattern = '(?P<base_name>.*)'
        for k, v in options.items():
            assert k.isidentifier(), f'Key: {k} is illegel.'
            assert isinstance(v, Iterable) and len(v) > 1, \
                    'All options should be Iterable and more than one.'
            for option in v:
                assert option.isidentifier(), f'Option: {option} is illegel.'
                assert isinstance(option, str), 'Only support str option.'
            if 'all' not in v:
                v.append('all')

            _pattern += '_(' + '?P<' + k + '>' + '|'.join(v) + ')'

        self._pattern = repr(_pattern)[1:-1]
        self._options = deepcopy(options)
        self._name = name
        self._uid = str(uuid.uuid1())

        self._module_dict = dict()
        columns = list(options.keys())
        columns.insert(0, 'base_name')
        self._module_infos = pd.DataFrame(columns=columns)

    @property
    def name(self):
        return self._name

    @property
    def pattern(self):
        return self._pattern

    @property
    def uid(self):
        return self._uid

    def __len__(self):
        return len(self._module_dict)

    def __repr__(self):
        return self.__class__.__name__ + \
                f'(name={self._name}, ' + \
                f'options={self._options}, ' + \
                f'module_dict={self._module_dict})'

    def __contains__(self, key: Any):
        if not isinstance(key, str):
            key = key.__name__
        return key in self._module_dict

    def __getitem__(self, key: str):
        module = self._module_dict[key]
        module_info = self._module_infos.loc[key].to_dict()
        return module, module_info

    def query(self, **kwargs):
        expr = []
        for k, v in kwargs.items():
            if isinstance(v, str):
                if v == 'all':
                    continue
                assert v.isidentifier()
                expr.append(k + '==' + repr(v))
            elif isinstance(v, list):
                if 'all' in v:
                    continue
                or_expr = []
                for _v in v:
                    assert isinstance(_v, str)
                    assert _v.isidentifier()
                    or_expr.append(k + '==' + repr(_v))
                expr.append('(' + '|'.join(or_expr) + ')')
            else:
                raise ValueError('The options only can be list or str')

        expr = '&'.join(expr)
        if not expr:
            module_infos = self._module_infos
        else:
            module_infos = self._module_infos.query(expr)
        return module_infos.copy()

    def match(self, module_or_str):
        if not isinstance(module_or_str, str):
            module_or_str = module_or_str.__name__

        match_results = re.match(self._pattern, module_or_str)
        if match_results is None:
            return None, None
        # to be continue

    def register_module(self, force: bool = False, module: Any = None):
        if module is not None:
            self._register(module, force=force)

        register_func = partial(self._register, force=force)
        return register_func

    def _register(self, module: Any, force: bool = False):
        full_name = module.__name__
        if not force and full_name in self._module_dict:
            raise ValueError(f'The module {module} has been registered.')

        if full_name in self._module_dict:
            infos = self._module_infos.loc[full_name].to_dict()
        else:
            match_objs = re.match(self._pattern, full_name)
            if match_objs is None:
                raise ValueError(f'The module name cannot match the pattern of {self._name}')

            infos = {k: match_objs.group(k) for k in self._options.keys()}
            infos['base_name'] = match_objs.group('base_name')
            self._module_infos.loc[full_name] = infos

        self._module_dict[full_name] = module
        self._update_uid()

    def _update_uid(self):
        self._uid = str(uuid.uuid1())
