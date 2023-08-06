# easytypes
Easy typed structures for Python with optional field checking and runtime type checking. Based on class decorators and ``typeguard`` package for type checking.

## What does the package implement
```
from easytypes import easy_type_decorator, safe_type, fast_type, unlimited_type
from easytypes import EasyTypesException
from easytypes import AttributeRequired, AttributeNotAllowed, AttributeTypeError
from easytypes import Required
from easytypes import disable_all_checks, enable_all_checks
```

## How to define a simple data class
```
from easytypes import easy_type_decorator, safe_type, fast_type, unlimited_type
from easytypes import EasyTypesException
from easytypes import AttributeRequired, AttributeNotAllowed, AttributeTypeError
from easytypes import Required
from easytypes import disable_all_checks, enable_all_checks

@safe_type  # You cannot: add new attrs; not set (or delete) the required attrs; assign wrong types
class A:
    a: int  # Type checking, not required, no default value
    b: str = '5'  # Type checking, not required, the default value is '5'
    c: float = Required()  # Type checking, required, no default value
    d: Tuple[int, int] = Required((2, 3))  # Type checking, required, the default value is (2, 3)
```
## ...and how does the class work
```
va = A(a=2, b='b', c=1.0, d=(2,4))  # Ok
assert va.a == 2
va.a = 5
assert va.a == 5
va = A(c=1.0)  # Ok, using default values
va = A(c=1.0, q=2)  # raises AttributeNotAllowed 
va.q = 0  # raises AttributeNotAllowed
va.a = '5'  # raises AttributeTypeError (a should be int)
va = A(c='c')  # raises AttributeTypeError (c should be float)
va = (b='c')  # raises AttributeRequired (a is missing)
```
## How to extend a class
```
@safe_type
class B(A):
    e: str = 5  # Is added to the fields defined in A
```
## ...and how to redefine a field
```
@safe_type
class C(A):
    a: int = 5  # Not recomended and not prohibited
```
## How to disable all the checks at runtime
```
disable_all_checks()  # Does not affect all the previously created classes, so put it before the class declaration
```
## ...and how to re-enable them
```
enable_all_checks()  # Does not affect all the previously created classes, so put it before the class declaration
```
## The other class decorators
```
unlimited_type  # Allows to add the attributes that are not declared at the class level
fast_type  # No checks at all, just a constructor implemetation accepting the attributes
```
## ...and how to get a customized decorator
```
easy_type_decorator(chk_required=True, chk_allowed=True, chk_types=True)  # Allows to activate only the desired checks
```
