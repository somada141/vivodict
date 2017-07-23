#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `vivodict` package."""

import pytest

from vivodict import VivoDict


@pytest.fixture(name="ref")
def fixture_ref():
    """Reference dictionary fixture."""
    ref = {"a": 1, "b": {"c": 2}, "d": {"e": {"f": 3}}}
    return ref


@pytest.fixture(name="ref_flattened_dots")
def fixture_ref_flattened_dots():
    """Flattened version of `ref` with a `.` delimiter."""
    ref_flattened_dots = {"a": 1, "b.c": 2, "d.e.f": 3}
    return ref_flattened_dots


@pytest.fixture(name="ref_flattened_dashes")
def fixture_ref_flattened_dashes():
    """Flattened version of `ref` with a `.` delimiter."""
    ref_flattened_dashes = {"a": 1, "b-c": 2, "d-e-f": 3}
    return ref_flattened_dashes


@pytest.fixture(name="ref_replaced_zeros")
def fixture_ref_replaced_zeros():
    """Replaced version of `ref` with a `replace_with` of `0`."""
    ref_replaced_zeros = {"a": 0, "b": {"c": 0}, "d": {"e": {"f": 0}}}
    return ref_replaced_zeros


@pytest.fixture(name="ref_applied_doubled")
def fixture_ref_applied_doubled():
    """Doubled version of `ref` with all values multiplied by `2`."""
    ref_applied_doubled = {"a": 2, "b": {"c": 4}, "d": {"e": {"f": 6}}}
    return ref_applied_doubled


def test_vivify(ref):
    """Test the `VivoDict.vivify` method."""

    vivo = VivoDict.vivify(dict_inp=ref)

    assert vivo == ref


def test_missing_is_vivodict(ref):
    """Test the `Vivodict.__missing__` override and asserts we get a
    `VivoDict`."""

    vivo = VivoDict.vivify(dict_inp=ref)

    # assert that we get a `VivoDict` for a missing key
    assert isinstance(vivo["missing"], VivoDict)


def test_missing_is_empty(ref):
    """Test the `Vivodict.__missing__` override and asserts we get an empty
    `VivoDict`."""

    vivo = VivoDict.vivify(dict_inp=ref)

    # assert that we get a `VivoDict` for a missing key
    assert vivo["missing"] == {}


def test_missing_nested(ref):
    """Test the `Vivodict.__missing__` override on nested missing keys."""

    vivo = VivoDict.vivify(dict_inp=ref)

    # assert that we get a `VivoDict` for the nested missing keys
    assert isinstance(vivo["missing"]["missing"]["missing"], VivoDict)


def test_flatten_default(ref, ref_flattened_dots):
    """Test the `VivoDict.flattened` method with default parameters."""

    vivo = VivoDict.vivify(dict_inp=ref)
    vivo_flattened = vivo.flatten()

    assert vivo_flattened == ref_flattened_dots


def test_flatten_dashes(ref, ref_flattened_dashes):
    """Test the `VivoDict.flattened` method with dash-delimiters."""

    vivo = VivoDict.vivify(dict_inp=ref)
    vivo_flattened = vivo.flatten(delimiter="-")

    assert vivo_flattened == ref_flattened_dashes


def test_replace_zeros(ref, ref_replaced_zeros):
    """Test the `VivoDict.flattened` method with dash-delimiters."""

    vivo = VivoDict.vivify(dict_inp=ref)
    # `replace` works in-place
    vivo.replace(replace_with=0)

    assert vivo == ref_replaced_zeros


def test_apply_double(ref, ref_applied_doubled):
    """Test the `VivoDict.flattened` method with dash-delimiters."""

    def double(value):
        return value * 2

    vivo = VivoDict.vivify(dict_inp=ref)
    # `apply` works in-place
    vivo.apply(func=double)

    assert vivo == ref_applied_doubled
