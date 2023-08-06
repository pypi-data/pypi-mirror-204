import contextlib
import io
import unittest
from unittest import mock
from unittest.mock import patch

import sys
import typing


class PassException(Exception):
    pass


class TestCase(unittest.TestCase):
    _termkit_arguments = []
    _termkit_expected_exception = None

    _termkit_with_capture_output = False

    _termkit_captured_stdout: io.StringIO = None
    _termkit_captured_stderr: io.StringIO = None
    termkit_expected_stdout: str = None
    termkit_expected_stderr: str = None

    def setUp(self) -> None:
        self.maxDiff = None
        self._termkit_captured_stdout = io.StringIO()
        self._termkit_captured_stderr = io.StringIO()
        self.termkit_expected_stdout: str = None
        self.termkit_expected_stderr: str = None

    def tearDown(self) -> None:
        if self._termkit_with_capture_output:
            self.assertEqual(self.termkit_expected_stdout, self._termkit_captured_stdout.getvalue())
            self.assertEqual(self.termkit_expected_stderr, self._termkit_captured_stderr.getvalue())
        self._termkit_captured_stdout = io.StringIO()
        self._termkit_captured_stderr = io.StringIO()

    @classmethod
    def tearDownClass(cls) -> None:
        cls._termkit_captured_stdout = io.StringIO()
        cls._termkit_captured_stderr = io.StringIO()

    def assertRaises(self, excClass, callableObj, *args, **kwargs):
        try:
            unittest.TestCase.assertRaises(self, PassException, callableObj, *args, **kwargs)
        except:
            print(f'>>> {repr(sys.exc_info()[1])}')
            self.assertEqual(f'{repr(self._termkit_expected_exception)}', f'{repr(sys.exc_info()[1])}')


def with_captured_output():
    """Marks test to expect the specified exception. Call assertRaises internally"""

    def test_decorator(fn):
        def test_decorated(self):
            with contextlib.redirect_stdout(self._termkit_captured_stdout):
                with contextlib.redirect_stdout(self._termkit_captured_stdout):
                    with patch.object(sys, 'argv', ['prog_name'] + self._termkit_arguments):
                        if len(self._termkit_arguments) > 0:
                            print(f'>>> call with arguments {self._termkit_arguments}')
                        else:
                            print(f'>>> call without arguments')
                        self._termkit_with_capture_output = True
                        return fn(self)

        return test_decorated

    return test_decorator


def with_assert_raises(exception):
    """Marks test to expect the specified exception. Call assertRaises internally"""

    def test_decorator(fn):
        def test_decorated(self, *args, **kwargs):
            self._termkit_expected_exception = exception
            self.assertRaises(type(exception), fn, self, *args, **kwargs)
            return self

        return test_decorated

    return test_decorator


def with_arguments(*arguments: str):
    """Marks test to expect the specified exception. Call assertRaises internally"""
    def test_decorator(fn):
        def test_decorated(self, *args, **kwargs):
            self._termkit_arguments = list(arguments)
            return fn(self)
        return test_decorated
    return test_decorator

# def with_arguments(*args: str):
#
#     def wrapper(func: typing.Callable, args=args):
#         func._termkit_arguments = list(map(str, args))
#         return func
#
#     return wrapper
