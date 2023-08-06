"""
Replacement for Bazel runfiles that can be used in pypi packages
"""
import importlib.resources
import pathlib
import sys

class runfiles:

    @classmethod
    def Create(cls):
        return cls

    @staticmethod
    def Rlocation(path):
        if sys.version_info[:2] >= (3, 10):
            return importlib.resources.files(__package__) / path
        else:
            for p in importlib.resources._get_package(__package__).__path__:
                file = pathlib.Path(p) / path
                if file.exists():
                    return file
