# -*- coding: utf-8 -*-

"""Main module."""


class VivoDict(dict):
    """ Auto-vivified dictionary class.

    This class derives `dict` and provides an auto-vivified dictionary with
    several convenince methods for converting arbitrarily nested `dict` objects
    into `VivoDict` objects as well as other operation such as flattening,
    setting all values to something, and applying a function to all values.

    This class essentially implements a tree with the added capability of adding
    and/or extending the branches upon access without raising a `KeyError` when
    a missing key is encountered.
    """

    def __missing__(self, key):
        """ Overrides `__missing__` built-in and provides autovivification.

        This method overrides the `__missing__` built-in of the `dict` class
        with code that will add a missing key and set it to an empty `VivoDict`
        object.

        Args:
            key: The missing dictionary key that would normally raise a
                `KeyError` exception.

        Returns:
            VivoDict: An empty `VivoDict` object instantiated upon encountering
                a missing key that would normally raise a `KeyError` exception.
        """

        # Create an empty `VivoDict` object and set it under the missing key
        # and the value that will be returned upon invocation.
        value = self[key] = type(self)()

        return value

    @classmethod
    def vivify(cls, dict_inp, _dict_out=None):
        """ Recursively transforms a nested `dict` into a `Vivodict`.

        This class method can be used to recursively convert an existing nested
        `dict` object to a `VivoDict` representation of itself. As a result any
        arbitrarily nested combination of existing/missing keys will either
        return an existing value or an empty `VivoDict` object (which is really
        an empty `dict`) and which evaluates to `False` in any boolean
        expression.

        Args:
            dict_inp (dict): The arbitrarily-nested `dict` object to be
                converted to a `VivoDict`.
            _dict_out (VivoDict): An INTERNAL `VivoDict` object that is used for
                this method's recursion. DO NOT SET THIS ARGUMENT.

        Returns:
            VivoDict: The converted `VivoDict` version of `dict_inp`.
        """

        # This condition should only pass during the inital method call (unless
        # someone didn't read the bloody docstring) and create an initial
        # `VivoDict` to be populated recursively as the original `dict_inp` is
        # being converted.
        if not _dict_out:
            _dict_out = VivoDict()

        # Iterate over the `dict_inp` items. If the `value` is another `dict`
        # then recurse over it and store the output under the given `key`.
        for key, value in dict_inp.items():
            if not isinstance(value, dict):
                _dict_out[key] = value
            else:
                _dict_out[key] = cls.vivify(dict_inp=value)

        return _dict_out

    def flatten(self, delimiter=".", _dummy=None):
        """Returns a flattened version of the dictionary.

        This method creates a flat `dict` version of the `VivoDict` where
        arbitrarily nested values are placed under a key delimited by the given
        `delimiter. A typical use-case is converting a nested dictionary of
        metrics into a flattened representation for use in Graphite metrics.

        Example:
            A simple example of flattening would be:

                >>> d = {"a": 1, "b": {"c": 2}, "d": {"e": {"f": 3}}}
                >>> v = VivoDict.vivify(d)
                >>> v.flatten()
                {'a': 1, 'b.c': 2, 'd.e.f': 3}

        Args:
            delimiter(str, optional): The delimiter to be inserted between the
                flattened keys. Defaults to ".".
            _dummy (VivoDict): An INTERNAL `VivoDict` object that is used for
                this method's recursion. DO NOT SET THIS ARGUMENT.

        Note:
            This method will only have an effect if the `VivoDict` object is
            nested.

        Returns:
            dict: The flattened version of the `VivoDict`.
        """

        # Create an empty `dict` that will store the flattened key-value pairs.
        dict_flattened = {}

        # This condition should only pass during the inital method call (unless
        # someone didn't read the bloody docstring) and set itself to the `self`
        # object which is to be flattened.
        if _dummy is None:
            _dummy = self

        # Iterate over the `_dummy` items. If the `value` is another `VivoDict`
        # then recurse over it and flatten its keys.
        for key, value in _dummy.items():
            if isinstance(value, type(self)):
                pairs_sub = self.flatten(
                    delimiter=delimiter,
                    _dummy=value
                )
                for key_sub, value_sub in pairs_sub.items():
                    key_flattened = "{0}{1}{2}".format(key, delimiter, key_sub)
                    dict_flattened[key_flattened] = value_sub
            else:
                dict_flattened[key] = value

        return dict_flattened

    def replace(self, replace_with, _dummy=None):
        """ Performs an in-place replacement of 'leaf' node values.

        This method performs a recursive in-place replacement of all 'leaf' node
        values with `replace_with`. Should you want to maintain the original
        `VivoDict` object's values I'd suggest you use the `copy` package prior
        to applying this method.

        Args:
            replace_with (object): Any object with which 'leaf' nodes will be
                replaced.
            _dummy: An INTERNAL `VivoDict` object that is used for
                this method's recursion. DO NOT SET THIS ARGUMENT.
        """

        # This condition should only pass during the inital method call (unless
        # someone didn't read the bloody docstring) and set itself to the `self`
        # object which is to be processed for replacement.
        if _dummy is None:
            _dummy = self

        # Iterate over the `_dummy` items. If the `value` is another `VivoDict`
        # then recurse over it and perform the replacement.
        for key, value in _dummy.items():
            if isinstance(value, type(self)):
                self.replace(replace_with=replace_with, _dummy=value)
            else:
                _dummy[key] = replace_with

    def apply(self, func, _dummy=None):
        """ Performs an in-place application of a function on 'leaf' values.

        This method performs a recursive in-place application and replacement of
        all 'leaf' node values with the return value of `func` upon it being
        applied on the original value. Should you want to maintain the original
        `VivoDict` object's values I'd suggest you use the `copy` package prior
        to applying this method.

        Args:
            func (function callable): The function to be applied on all 'leaf'
                node values, the return value of which will replace those
                values.
            _dummy: An INTERNAL `VivoDict` object that is used for
                this method's recursion. DO NOT SET THIS ARGUMENT.
        """

        if _dummy is None:
            _dummy = self

        for key, value in _dummy.items():
            if isinstance(value, type(self)):
                self.apply(func=func, _dummy=value)
            else:
                _dummy[key] = func(_dummy[key])
