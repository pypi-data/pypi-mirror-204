# -*- coding: utf-8 -*-
"""Package helper functions and classes.

Copyright (c) 2021 Cisco and/or its affiliates.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


from __future__ import absolute_import, division, print_function, unicode_literals

from future import standard_library

standard_library.install_aliases()
native_str = str

import json
import mimetypes
import os
import sys
import urllib.parse
from base64 import b64decode
from builtins import *
from collections import OrderedDict, namedtuple
from datetime import datetime, timedelta, tzinfo

import xmltodict
from past.builtins import basestring

EncodableFile = namedtuple('EncodableFile',
                           ['file_name', 'file_object', 'content_type'])


def to_unicode(string):
    """Convert a string (bytes, str or unicode) to unicode."""
    assert isinstance(string, basestring)
    if sys.version_info[0] >= 3:
        if isinstance(string, bytes):
            return string.decode('utf-8')
        else:
            return string
    else:
        if isinstance(string, str):
            return string.decode('utf-8')
        else:
            return string


def to_bytes(string):
    """Convert a string (bytes, str or unicode) to bytes."""
    assert isinstance(string, basestring)
    if sys.version_info[0] >= 3:
        if isinstance(string, str):
            return string.encode('utf-8')
        else:
            return string
    else:
        if isinstance(string, unicode):
            return string.encode('utf-8')
        else:
            return string


def validate_base_url(base_url):
    """Verify that base_url specifies a protocol and network location."""
    parsed_url = urllib.parse.urlparse(base_url)
    if parsed_url.scheme and parsed_url.netloc:
        return parsed_url.geturl()
    else:
        error_message = "base_url must contain a valid scheme (protocol " \
                        "specifier) and network location (hostname)"
        raise ValueError(error_message)


def is_web_url(string):
    """Check to see if string is an validly-formatted web url."""
    assert isinstance(string, basestring)
    parsed_url = urllib.parse.urlparse(string)
    return (
        (
            parsed_url.scheme.lower() == 'http'
            or parsed_url.scheme.lower() == 'https'
        )
        and parsed_url.netloc
    )


def is_local_file(string):
    """Check to see if string is a valid local file path."""
    assert isinstance(string, basestring)
    return os.path.isfile(string)


def open_local_file(file_path):
    """Open the file and return an EncodableFile tuple."""
    assert isinstance(file_path, basestring)
    assert is_local_file(file_path)
    file_name = os.path.basename(file_path)
    file_object = open(file_path, 'rb')
    content_type = mimetypes.guess_type(file_name)[0] or 'text/plain'
    return EncodableFile(file_name=file_name,
                         file_object=file_object,
                         content_type=content_type)


def check_type(o, acceptable_types, may_be_none=True):
    """Object is an instance of one of the acceptable types or None.

    Args:
        o: The object to be inspected.
        acceptable_types: A type or tuple of acceptable types.
        may_be_none(bool): Whether or not the object may be None.

    Raises:
        TypeError: If the object is None and may_be_none=False, or if the
            object is not an instance of one of the acceptable types.

    """
    if not isinstance(acceptable_types, tuple):
        acceptable_types = (acceptable_types,)

    if may_be_none and o is None:
        # Object is None, and that is OK!
        pass
    elif isinstance(o, acceptable_types):
        # Object is an instance of an acceptable type.
        pass
    elif isinstance(o, list):
        # Object is an instance of an list.
        if len(o)>0 and len(o)<2 and isinstance(o[0], acceptable_types):
            pass
        else:
            # Object is something else.
            error_message = (
                "We were expecting to receive an instance of one of the following "
                "types: {types}{none}; but instead we received {o} which is a "
                "{o_type}.".format(
                    types=", ".join([repr(t.__name__) for t in acceptable_types]),
                    none="or 'None'" if may_be_none else "",
                    o=o,
                    o_type=repr(type(o).__name__)
                )
            )
            raise TypeError(error_message)
    else:
        # Object is something else.
        error_message = (
            "We were expecting to receive an instance of one of the following "
            "types: {types}{none}; but instead we received {o} which is a "
            "{o_type}.".format(
                types=", ".join([repr(t.__name__) for t in acceptable_types]),
                none="or 'None'" if may_be_none else "",
                o=o,
                o_type=repr(type(o).__name__)
            )
        )
        raise TypeError(error_message)


def dict_from_items_with_values(*dictionaries, **items):
    """Creates a dict with the inputted items; pruning any that are `None`.

    Args:
        *dictionaries(dict): Dictionaries of items to be pruned and included.
        **items: Items to be pruned and included.

    Returns:
        dict: A dictionary containing all of the items with a 'non-None' value.

    """
    dict_list = list(dictionaries)
    dict_list.append(items)
    result = {}
    for d in dict_list:
        for key, value in d.items():
            if value is not None:
                result[key] = value
    return result


def raise_if_extra_kwargs(kwargs):
    """Raise a TypeError if kwargs is not empty."""
    if kwargs:
        raise TypeError("Unexpected **kwargs: {!r}".format(kwargs))


def extract_and_parse(response):
    if 'application/json' in response.headers.get('Content-Type', []):
        return extract_and_parse_json(response)
    elif 'application/xml' in response.headers.get('Content-Type', []):
        return extract_and_parse_xml(response)
    return response.text


def extract_and_parse_json(response):
    """Extract and parse the JSON data from an requests.response object.

    Args:
        response(requests.response): The response object returned by a request
            using the requests package.
        stream(bool): If the request was to get a raw response content

    Returns:
        The parsed JSON data as the appropriate native Python data type.

    Raises:
        JSONDecodeError: caused by json.loads
        TypeError: caused by json.loads
    """
    if response.text:
        try:
            return json.loads(response.text, object_hook=OrderedDict)
        except Exception as e:
            raise e
    else:
        return None


def extract_and_parse_xml(response):
    result = None
    if response.text:
        try:
            result = xmltodict.parse(response.text)
        except Exception:
            result = None
        return result
    else:
        return None


def json_dict(json_data):
    """Given a dictionary or JSON string; return a dictionary.

    Args:
        json_data(dict, str): Input JSON object.

    Returns:
        A Python dictionary with the contents of the JSON object.

    Raises:
        TypeError: If the input object is not a dictionary or string.

    """
    if isinstance(json_data, dict):
        return json_data
    elif isinstance(json_data, basestring):
        return json.loads(json_data, object_hook=OrderedDict)
    elif isinstance(json_data, list):
        return json_data
    else:
        raise TypeError(
            "'json_data' must be a dictionary or valid JSON string; "
            "received: {!r}".format(json_data)
        )


def apply_path_params(URL, path_params):
    if isinstance(URL, str) and isinstance(path_params, dict):
        for k in path_params:
            URL = URL.replace('${' + k + '}', str(path_params[k]))
            URL = URL.replace('{' + k + '}', str(path_params[k]))
        return URL
    else:
        raise TypeError(
            "'URL' must be a string; "
            "'path_params' must be a dictionary or valid JSON string; "
            "received: (URL={}, path_params={})".format(URL, path_params)
        )


def pprint_request_info(url, method, _headers, **kwargs):
    debug_print = (
        "\nRequest"
        "\n\tURL: {}"
        "\n\tMethod: {}"
        "\n\tHeaders: \n{}"
    )
    _headers.update(kwargs.get('headers', {}))
    _headers = '\n'.join(['\t\t{}: {}'.format(a, b)
                         for a, b in _headers.items()])
    debug_print = debug_print.format(url, method, _headers)

    kwargs_to_include = ['params', 'json', 'data', 'stream']
    kwargs_pprint = {
        'params': 'Params', 'json': 'Body',
        'data': 'Body', 'stream': 'Stream'
    }

    for kw in kwargs_to_include:
        if kwargs.get(kw) is not None and kwargs_pprint.get(kw):
            value = kwargs.get(kw)
            key = kwargs_pprint.get(kw)
            if isinstance(value, list) or isinstance(value, dict):
                value = json.dumps(value, indent=4)
                lines = [' ' * (8 + len(key)) + line
                         for line in value.split('\n')]
                value = '\n'.join(lines)
            else:
                value = '\t\t{}'.format(value)

            format_str = '{}\n\t{}:\n{}'
            debug_print = format_str.format(debug_print,
                                            key,
                                            value)
    return debug_print


def pprint_response_info(response):
    if response is None:
        return ""

    debug_print = (
        "\nResponse"
        "\n\tStatus: {} - {}"
        "\n\tHeaders: \n{}"
    )
    headers = response.headers
    headers = '\n'.join(['\t\t{}: {}'.format(a, b)
                         for a, b in headers.items()])
    body = None
    file_resp_headers = ['Content-Disposition', 'fileName']

    if 'application/json' in response.headers.get('Content-Type', []):
        try:
            body = response.json()
            body = json.dumps(body, indent=4)
            body = '\n'.join([' ' * 13 + line for line in body.split('\n')])
        except Exception:
            body = response.text or response.content
            pass
    elif any([i in response.headers for i in file_resp_headers]):
        body = None
    else:
        body = response.text or response.content

    debug_print = debug_print.format(response.status_code,
                                     response.reason,
                                     headers)

    if body is not None:
        format_str = '{}\n\t{}:\n{}'
        debug_print = format_str.format(debug_print, 'Body', body)

    return debug_print


def dict_of_str(json_dict):
    """Given a dictionary; return a new dictionary with all items as strings.

    Args:
        json_dict(dict): Input JSON dictionary.

    Returns:
        A Python dictionary with the contents of the JSON object as strings.
    """
    result = {}
    for key, value in json_dict.items():
        result[key] = '{}'.format(value)
    return result


def walk_through_dict(resp, access_next_list, omit_first_single_key=False):
    """ Walks through a dict `resp`
    in the order of the `access_next_list` (list of str)
    by accessing the items in order.
    If `omit_first_single_key` is set to True if resp is a dict
    with a single key it will access (omitting the first access_next_list)
    """
    value = resp
    found = True
    if isinstance(value, str):
        return (found, value)

    if len(access_next_list) == 0:
        return (False, None)

    if isinstance(value, dict) and omit_first_single_key and len(value) == 1:
        access_key = access_next_list[0]
        key = list(value.keys())[0]
        if key == access_key:
            access_next_list = access_next_list[1:]
        value = value.get(key)

    for access_next in access_next_list:
        if isinstance(value, dict):
            if value.get(access_next):
                value = value.get(access_next)
            else:
                value = None
                break
        elif isinstance(value, list) and len(value) > 0 and access_next == "[0]":
            value = value[0]
    if not isinstance(value, str):
        found = False
    return (found, value)


def get_err_message(err_response, access_next_list):
    (found, value) = walk_through_dict(err_response, access_next_list, omit_first_single_key=True)
    return value if found else None


def extract_authorization_data(authorization_header):
    authorization_data = ""
    authorization_header_ = bytes(authorization_header.replace('Basic ', ''), 'utf-8')
    authorization_header_ = b64decode(authorization_header_)
    authorization_header_str = authorization_header_.decode('utf-8')
    elements = authorization_header_str.split(':')
    if len(elements) == 2:
        (username, password) = elements
        authorization_data = "\nUsername: {username}\nPassword: {password}\n".format(
            username=username,
            password=password)
    return authorization_data


def get_exception_additional_data(**kwargs):
    additional_data = ""
    headers = kwargs.get('headers')
    response = kwargs.get('response')
    _headers = {}
    status_code_to_give_credentials = [401, 403]
    headers_with_credentials = ['Authorization', 'X-CSRF-Token']

    if hasattr(response, 'status_code'):
        if response.status_code in status_code_to_give_credentials:
            if headers:
                for sensitive_header in headers_with_credentials:
                    if headers.get(sensitive_header):
                        _headers[sensitive_header] = headers[sensitive_header]
                additional_data += '\n'.join(['{}: {}'.format(a, b) for a, b in _headers.items()])

    authorization_header = _headers.get('authorization') or _headers.get('Authorization') or ''
    if authorization_header:
        additional_data += extract_authorization_data(authorization_header)
    return additional_data
