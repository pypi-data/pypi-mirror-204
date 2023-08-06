import inspect
from typing import Any, Type, Dict

import typeguard

_DISABLE_ALL_CHECKS = False


def disable_all_checks() -> None:
    global _DISABLE_ALL_CHECKS
    _DISABLE_ALL_CHECKS = True


def enable_all_checks() -> None:
    global _DISABLE_ALL_CHECKS
    _DISABLE_ALL_CHECKS = False


class EasyTypesException(Exception):
    ...


class AttributeNotAllowed(AttributeError, EasyTypesException):
    def __init__(self, obj: Any, attrname: str):
        super().__init__(f"Object {obj.__class__.__name__} should not have an attibute named '{attrname}'")


class AttributeRequired(AttributeError, EasyTypesException):
    def __init__(self, obj: Any, *a: str):
        super().__init__(f"Object {obj.__class__.__name__} should have the following attributes: '{', '.join(a)}'")


class AttributeTypeError(TypeError, EasyTypesException):
    def __init__(self, obj: Any, attrname: str, value: Any, ct: Type):
        super().__init__(
            f"{obj.__class__.__name__}.__class__.{attrname} cannot accept a value of type "
            f"{value.__class__.__name__}, expected {ct}")


class NoValue:
    ...


class Required:
    def __init__(self, val: Any = NoValue):
        self.value = val


def easy_type_decorator(chk_required=True, chk_allowed=True, chk_types=True):
    def wrapper(cls):
        chk_r, chk_a, chk_t = (False, False, False) if _DISABLE_ALL_CHECKS else (chk_required, chk_allowed, chk_types)
        required, allowed, check_types, default_values = set(), set(), {}, {}
        bases = [c for c in inspect.getmro(cls) if not c is object]
        bases.reverse()  # Move from base classes to the derived ones for proper overriding...
        for c in bases:
            for k, val in c.__dict__.items():
                if not k.startswith('__'):
                    if k in required:
                        required.remove(k)
                    if k in default_values:
                        del default_values[k]
                    if k in check_types:
                        del check_types[k]
                    allowed.add(k)
                    dval = val
                    if isinstance(val, Required):
                        required.add(k)
                        dval = val.value
                    if dval is not NoValue:
                        default_values[k] = dval
            for k, t in c.__annotations__.items():
                if k not in c.__dict__:
                    required.discard(k)
                    if k in default_values:
                        del default_values[k]
                allowed.add(k)
                check_types[k] = t

        def _init(self, **kw: Dict[str, Any]) -> None:
            for a, v in kw.items():
                setattr(self, a, v)
            for a, v in default_values.items():
                if a not in kw:
                    setattr(self, a, v)
            if chk_r:
                if r := required.difference(set(kw.keys())).difference(set(default_values.keys())):
                    raise AttributeRequired(self, *r)

        def _setattr(self, attrname: str, val: Any) -> None:
            if chk_a and attrname not in allowed:
                raise AttributeNotAllowed(self, attrname)
            if chk_t and ((ct := check_types.get(attrname, NoValue)) is not NoValue):
                try:
                    typeguard.check_type(val, ct)
                except typeguard.TypeCheckError:
                    raise AttributeTypeError(self, attrname, val, ct)
            object.__setattr__(self, attrname, val)

        def _delattr(self, attrname: str) -> None:
            if chk_r and attrname in required:
                raise AttributeRequired(self, attrname)
            object.__delattr__(self, attrname)

        def _str(self) -> str:
            keys = list(self.__dict__.keys())
            keys.sort()  # We need the results to be repeatable
            return f"<{self.__class__.__name__} {', '.join(f'{k}={self.__dict__[k]!r}' for k in keys)}>"

        methods = {"__init__": _init, "__str__": _str, "__repr__": _str,
                   "__setattr__": _setattr, "__delattr__": _delattr}
        return type(f"_easy_type.{cls.__name__}", (cls,), methods)

    return wrapper


fast_type = easy_type_decorator(False, False, False)  # No checks, just the attribute machinery
unlimited_type = easy_type_decorator(True, False, True)  # Checks on, extra attrs allowed
safe_type = easy_type_decorator()  # All checks on
