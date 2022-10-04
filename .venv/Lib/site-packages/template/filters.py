#!/usr/bin/env python
"""Filters for the template CLI."""
# pylint: disable=import-error, import-outside-toplevel


from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)  # pylint: disable=duplicate-code

from template.functions import run  # noqa: F401 pylint: disable=unused-import


def to_yaml(value):
    r"""
    Converts given data structure to YAML form.
    Examples:

    >>> to_yaml([1,2,3])
    '- 1\n- 2\n- 3\n'
    >>> to_yaml({'a': 1, 'b': 2})
    'a: 1\nb: 2\n'
    >>> to_yaml({1: {'a': [1,2,3]}})
    '1:\n  a:\n  - 1\n  - 2\n  - 3\n'
    >>> to_yaml("abc")
    'abc\n...\n'
    """
    from yaml import safe_dump

    return safe_dump(value)


def to_json(value):
    """
    Converts given data structure to JSON form.
    Examples:

    >>> to_json([1,2,3])
    '[1, 2, 3]'
    >>> to_json({'b':2})
    '{"b": 2}'
    >>> to_json(2)
    '2'
    >>> to_json({1: {'a': [1,2,3]}})
    '{"1": {"a": [1, 2, 3]}}'
    """
    from json import dumps

    return dumps(value)


def from_json(value):
    """
    Returns native data structure from the given JSON string.
    Examples:

    >>> import six
    >>> from_json('[1, 2, 3]')
    [1, 2, 3]
    >>> from_json('"a"') == six.text_type('a')
    True
    >>> from_json('{"1": {"a": [1, 2, 3]}}') == {'1': {'a': [1, 2, 3]}}
    True
    """
    from json import loads

    return loads(value)


def from_yaml(value):
    """
    Returns native data structure from the given YAML string.
    Examples:

    >>> from_yaml('a')
    'a'
    >>> from_yaml('[1, 2, 3]')
    [1, 2, 3]
    >>> from_yaml('{"1": {"a": [1, 2, 3]}}')
    {'1': {'a': [1, 2, 3]}}
    """
    from yaml import safe_load

    return safe_load(value)


def combine(default, override):
    """
    Returns a combined dictionary of the 2 dictionaries given (with the 2nd
    overriding the 1st).
    Examples:
    >>> combine({'a': 1, 'b': 2}, {'b': 3, 'c': 4}) == {'a': 1, 'b': 3, 'c': 4}
    True
    """
    combined = default.copy()
    combined.update(override)
    return combined


def from_toml(value):
    """
    Returns a data structure from the TOML string given.
    Examples:
    >>> from_toml('[table]\\nkey = "value"\\n') == {'table': {'key': 'value'}}
    True
    """
    from toml import loads

    return loads(value)


def to_toml(value):
    """
    Returns a string of the TOML representation for the data structure given.
    Examples:
    >>> import six
    >>> to_toml({'key': [1, 2]}) == six.text_type("key = [ 1, 2,]\\n")
    True
    """
    from toml import dumps

    return dumps(value)


def jmespath(value, query):
    """
    Queries the data using the JMESPath query language.
    Examples:
    >>> import six
    >>> locations = [{'name': 'Seattle', 'state': 'WA'},
    ... {"name": "New York", "state": "NY"},
    ... {"name": "Bellevue", "state": "WA"},
    ... {"name": "Olympia", "state": "WA"}]
    >>> query = "[?state == 'WA'].name | sort(@) | {WashingtonCities: join(', ', @)}"  # noqa: E501
    >>> WACities = jmespath(locations, query)
    >>> if six.PY2:
    ...  WACities == {u'WashingtonCities': u'Bellevue, Olympia, Seattle'}
    ... elif six.PY3:
    ...  WACities == {'WashingtonCities': 'Bellevue, Olympia, Seattle'}
    ...
    True
    """
    import jmespath as jp

    return jp.search(query, value)


def ipaddress(addr, version=None, flags=0):
    """
    Returns an IPAddress object from the netaddr library.

    >>> ip = ipaddress('10.0.0.1')
    >>> type(ip)
    <class 'netaddr.ip.IPAddress'>
    >>> ip.is_private()
    True
    """

    from netaddr import IPAddress

    return IPAddress(addr, version, flags)


def ipglob(glob):
    """
    Returns an IPGlob object from the netaddr library.

    >>> glob = ipglob("192.168.32.*")
    >>> type(glob)
    <class 'netaddr.ip.glob.IPGlob'>
    >>> glob.is_private()
    True
    """

    from netaddr import IPGlob

    return IPGlob(glob)


def ipnetwork(addr, implicit_prefix=False, version=None, flags=0):
    """
    Returns an IPNetwork object from the netaddr library.

    >>> net = ipnetwork("172.32.0.0/24")
    >>> type(net)
    <class 'netaddr.ip.IPNetwork'>
    >>> net.is_private()
    False
    """

    from netaddr import IPNetwork

    return IPNetwork(addr, implicit_prefix, version, flags)


def iprange(start, end, flags=0):
    """
    Returns an IPRange object from the netaddr library.

    >>> range = iprange("1.2.3.0", "1.2.3.255")
    >>> type(range)
    <class 'netaddr.ip.IPRange'>
    >>> len(range)
    256
    """

    from netaddr import IPRange

    return IPRange(start, end, flags)


def ipset(iterable=None, flags=0):
    """
    Returns an IPSet object from the netaddr library.

    >>> ipset = ipset(["10.0.0.0/16"])
    >>> type(ipset)
    <class 'netaddr.ip.sets.IPSet'>
    >>> ipaddress('10.0.0.1') in ipset
    True
    """

    from netaddr import IPSet

    return IPSet(iterable, flags)
