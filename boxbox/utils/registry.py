from collections.abc import Iterable
from typing import Dict, List, Any


class Registrar:

    def __init__(self, name: str, distinguish: Dict[Any, List[str]] = None):
        self._name = name
        self._distinguish = dict()
        self._module_dict = dict()

        if distinguish is not None:
            for k, v in distinguish.items():
                assert isinstance(v, Iterable) and len(v) > 1, \
                        'The options should be Iterable and more than one.'
                for option in v:
                    assert isinstance(option, str), 'Only support str option.'

                self._distinguish[k] = v

        self._pattern

        

    def __repr__(self):
        format_str = self.__class__.__name__ + \
                f'(name={self._name}, ' + \
                f'distinguish={self._distinguish}, ' + \
                f'_module_dict={self._module_dict})'

    def register_module(self, options: Dict[Any]):
        pass
