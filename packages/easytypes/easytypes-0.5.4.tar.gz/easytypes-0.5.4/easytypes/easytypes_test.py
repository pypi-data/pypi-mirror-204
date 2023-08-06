import unittest

from easytypes import easy_type_decorator, safe_type, fast_type, unlimited_type
# from easytypes import EasyTypesException
from easytypes import AttributeRequired, AttributeNotAllowed, AttributeTypeError
from easytypes import Required
from easytypes import disable_all_checks, enable_all_checks


class MyTestCase(unittest.TestCase):
    def test_safe_type(self):
        @safe_type
        class MyType:
            a: int
            b: str = Required()
            c: str = Required("default_str")
            d: str = "default_str"

        mt1 = MyType(a=1, b='string')
        self.assertEqual(str(mt1), "<_easy_type.MyType a=1, b='string', c='default_str', d='default_str'>")
        mt1.a = 2
        mt1.b = "some_string"
        mt1.c = "one_more_string"
        mt1.d = "and_the_final_one"
        self.assertEqual(repr(mt1),
                         "<_easy_type.MyType a=2, b='some_string', c='one_more_string', d='and_the_final_one'>")
        del mt1.a
        self.assertEqual(repr(mt1), "<_easy_type.MyType b='some_string', c='one_more_string', d='and_the_final_one'>")
        self.assertRaises(AttributeRequired, MyType, a=1)
        self.assertRaises(AttributeRequired, delattr, mt1, 'b')
        self.assertRaises(AttributeNotAllowed, setattr, mt1, 'q', 1)
        self.assertRaises(AttributeNotAllowed, MyType, q=1)
        self.assertRaises(AttributeTypeError, setattr, mt1, "c", 1)
        self.assertRaises(AttributeTypeError, setattr, mt1, "d", 1)

    def test_disable_checks(self):
        disable_all_checks()
        try:
            @safe_type
            class MyType:
                a: int
                b: str = Required()
                c: str = Required("default_str")
                d: str = "default_str"

            enable_all_checks()  # No effect on the previously created classes
            mt1 = MyType(a=1, b='string')
            self.assertEqual(repr(MyType(a=1)), "<_easy_type.MyType a=1, c='default_str', d='default_str'>")
            del mt1.b
            self.assertEqual(repr(mt1), "<_easy_type.MyType a=1, c='default_str', d='default_str'>")
            mt1.q = 1
            self.assertEqual(repr(mt1), "<_easy_type.MyType a=1, c='default_str', d='default_str', q=1>")
            self.assertEqual(repr(MyType(q=1)), "<_easy_type.MyType c='default_str', d='default_str', q=1>")
            mt1.c = 1
            mt1.d = 1
            self.assertEqual(repr(mt1), "<_easy_type.MyType a=1, c=1, d=1, q=1>")
        finally:
            enable_all_checks()

    def test_unlimited(self):
        @unlimited_type
        class MyType:
            a = Required(1)

        mt = MyType(q=5)
        self.assertRaises(AttributeRequired, delattr, mt, 'a')

    def test_fast(self):
        @fast_type
        class MyType:
            a: int
            b: str = Required()
            c: str = Required("default_str")
            d: str = "default_str"

        mt1 = MyType(a=1, b='string')
        self.assertEqual(repr(MyType(a=1)), "<_easy_type.MyType a=1, c='default_str', d='default_str'>")
        del mt1.b
        self.assertEqual(repr(mt1), "<_easy_type.MyType a=1, c='default_str', d='default_str'>")
        mt1.q = 1
        self.assertEqual(repr(mt1), "<_easy_type.MyType a=1, c='default_str', d='default_str', q=1>")
        self.assertEqual(repr(MyType(q=1)), "<_easy_type.MyType c='default_str', d='default_str', q=1>")
        mt1.c = 1
        mt1.d = 1
        self.assertEqual(repr(mt1), "<_easy_type.MyType a=1, c=1, d=1, q=1>")

    def test_no_partial_inheritance(self):
        @safe_type
        class A:
            a: int = Required(1)
            b: int = Required()
            c: int = 3

        @safe_type
        class B(A):
            a = 's'
            b: str
            c: str

        b = B(a='1', b='2')
        self.assertFalse('c' in b.__dict__)

    def test_inheritance(self):
        @safe_type
        class A:
            a: str = Required()
            a1: str = 'a1'
            a2 = Required()

        @safe_type
        class B(A):
            b: str = Required()
            a1: int = Required(2)
            a2: int = 2

        self.assertRaises(AttributeRequired, B, b='b')
        self.assertRaises(AttributeRequired, B, a='a')
        self.assertRaises(AttributeTypeError, B, a='a', b='b', a1='a1')
        b1 = B(a='a', b='b')
        self.assertEqual(repr(b1), "<_easy_type.B a='a', a1=2, a2=2, b='b'>")
        self.assertRaises(AttributeRequired, delattr, b1, 'a1')
        self.assertRaises(AttributeTypeError, setattr, b1, 'a2', 'a')


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
