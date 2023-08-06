#
# File:    ./tests/unit/utils.py
# Author:  Jiří Kučera <sanczes AT gmail.com>
# Date:    2021-09-22 23:46:47 +0200
# Project: vutils-testing: Auxiliary library for writing tests
#
# SPDX-License-Identifier: MIT
#
"""
Unit tests utilities.

:const FOO_CONSTANT: The auxiliary constant used in tests

.. |cover_typing| replace:: :func:`~vutils.testing.utils.cover_typing`
"""

import io
import sys

from vutils.testing.mock import PatcherFactory

FOO_CONSTANT = 42


class FooError(Exception):
    """
    Dummy exception.

    :ivar detail: The error detail
    """

    __slots__ = ("detail",)

    def __init__(self, detail):
        """
        Initialize the exception object.

        :param detail: The error detail
        """
        Exception.__init__(self, detail)
        self.detail = detail


class StderrPatcher(PatcherFactory):
    """
    :mod:`sys.stderr` patcher.

    :ivar stream: The new error stream
    """

    __slots__ = ("stream",)

    def setup(self):
        """Set up the patcher."""
        self.stream = io.StringIO()
        self.add_spec("sys.stderr", new=self.stream)


class StderrWriter:
    """
    Dummy standard error output writer.

    :ivar stream: The error stream to write
    :ivar code: The error code
    :ivar label: The label of an error message
    """

    __slots__ = ("stream", "code", "label")

    def __init__(self, code, label=""):
        """
        Initialize the writer.

        :param code: The code
        :param label: The label
        """
        self.stream = sys.stderr
        self.code = code
        self.label = label

    @staticmethod
    def format(code, label, text):
        """
        Format the message.

        :param code: The code
        :param label: The label
        :param text: The text
        :return: the formatted message
        """
        return f"({code})[{label}] {text}\n"

    def write(self, text):
        """
        Write :arg:`text` to stream.

        :param text: The text
        """
        self.stream.write(self.format(self.code, self.label, text))


class DummyPatch:
    """
    Dummy :func:`unittest.mock.patch` implementation.

    :ivar __owner: The owner of the instance
    :ivar __context: The *context* (arguments passed to the constructor)
    """

    __slots__ = ("__owner", "__context")

    def __init__(self, owner, target, *args, **kwargs):
        """
        Initialize the patch.

        :param owner: The owner of this instance
        :param target: The target to be patched
        :param args: Additional positional arguments
        :param kwargs: Additional key-value arguments
        """
        self.__owner = owner
        self.__context = (target, args, kwargs)

    def start(self):
        """
        Start the patching procedure.

        Actually only log the action.
        """
        self.__owner.log.append(("start", self.__context))

    def stop(self):
        """
        Restore changes done by the patching procedure.

        Actually only log the action.
        """
        self.__owner.log.append(("stop", self.__context))


class CoverTypingPatcher(PatcherFactory):
    """
    Patcher that patches objects used by |cover_typing|.

    :ivar modules: The dictionary of imported-like modules
    :ivar log: The log of performed actions
    """

    __slots__ = ("modules", "log")

    def mock_import_module(self, name):
        """
        Import the module :arg:`name`.

        :param name: The name of the module to be imported
        :return: the imported module

        Partially mock the behavior of :func:`importlib.import_module`.
        """
        if name in self.modules:
            return self.modules[name]
        path = []
        for part in name.split("."):
            module = type(sys)(part)
            if path:
                parent = self.modules[".".join(path)]
                setattr(parent, part, module)
            path.append(part)
            self.modules[".".join(path)] = module
        return self.modules[".".join(path)]

    def mock_reload(self, module):
        """
        Reload :arg:`module`.

        :param module: The module to be reloaded

        Actually only log the reload event.
        """
        self.log.append(("reload", module))

    def mock_patch(self, target, *args, **kwargs):
        """
        Make a patch for :arg:`target`.

        :param target: The target to be patched
        :param args: Additional positional arguments
        :param kwargs: Additional key-value arguments
        :return: the patch
        """
        return DummyPatch(self, target, *args, **kwargs)

    def setup(self):
        """Set up the patcher."""
        self.modules = {}
        self.log = []

        self.add_spec("importlib.import_module", new=self.mock_import_module)
        self.add_spec("importlib.reload", new=self.mock_reload)
        self.add_spec("vutils.testing.mock.make_patch", new=self.mock_patch)


def func_a(mock):
    """
    Modify :arg:`mock`.

    :param mock: The mock object
    """
    mock.foo = FOO_CONSTANT


def func_b(mock):
    """
    Modify :arg:`mock` and raise :exc:`.FooError`.

    :param mock: The mock object
    :raises .FooError: when called
    """
    func_a(mock)
    raise FooError(FOO_CONSTANT)
