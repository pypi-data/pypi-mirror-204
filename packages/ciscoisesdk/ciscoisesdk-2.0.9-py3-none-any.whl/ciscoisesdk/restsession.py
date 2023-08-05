# -*- coding: utf-8 -*-
"""RestSession class for creating connections to the Identity Services Engine APIs.

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

import errno
import logging
import os
import re
import socket
import time
import urllib.parse
import warnings
from builtins import *

import requests
from past.builtins import basestring
from requests.packages.urllib3.response import HTTPResponse
from requests_toolbelt.multipart import encoder

from .config import (
    DEFAULT_SINGLE_REQUEST_TIMEOUT,
    DEFAULT_VERIFY,
    DEFAULT_WAIT_ON_RATE_LIMIT,
)
from .exceptions import (
    ApiError,
    DownloadFailure,
    RateLimitError,
    RateLimitWarning,
    ciscoisesdkException,
)
from .misc import check_response_code
from .response_codes import EXPECTED_RESPONSE_CODE
from .restresponse import RestResponse
from .utils import (
    check_type,
    get_exception_additional_data,
    pprint_request_info,
    pprint_response_info,
    validate_base_url,
)

logger = logging.getLogger(__name__)


class DownloadResponse(HTTPResponse):
    """Download Response wrapper.

    Bases: urllib3.response.HTTPResponse. For more
    information check the `urlib3 documentation <https://urllib3.readthedocs.io/en/latest/reference/urllib3.response.html>`_

    HTTP Response container.
    """

    def __init__(self, response, path, filename, dirpath, collected_data):
        """
        Creates a new DownloadResponse object.

        By calling urllib3.response.HTTPResponse __init__ method
        with the raw property of requests.Response,
        it recovers data from the API response

        It adds properties regarding the download: filename, dirpath and path

        Args:
            response(requests.Response): The Response object, which contains a server's
                response to an HTTP request.
            path(basestring): The downloaded file path.
            filename(basestring): The downloaded filename.
            dirpath(basestring): The download directory path.
            collected_data(bytes): HTTP response's data.
        """
        super(DownloadResponse, self).__init__(
            body=response.raw,
            headers=response.headers,
            status=response.status_code,
            reason=response.reason,
            request_method=response.request.method,
            request_url=response.request.url,
        )
        # adds additional and important information
        self._filename = filename
        self._dirpath = dirpath
        self._path = path
        self._collected_data = collected_data

    @property
    def data(self):
        """The HTTPResponse's data"""
        # Call HTTPResponse's data property
        original_data = super(DownloadResponse, self).data
        # It uses the one that has value prioritizing the HTTPResponse's data
        return original_data or self._collected_data

    @property
    def filename(self):
        """The downloaded filename"""
        return self._filename

    @property
    def dirpath(self):
        """The downloaded directory path"""
        return self._dirpath

    @property
    def path(self):
        """The download file path"""
        return self._path


# Main module interface
class RestSession(object):
    """RESTful HTTP session class for making calls to the Identity Services Engine APIs."""

    def __init__(self, get_access_token, access_token, base_url,
                 single_request_timeout=DEFAULT_SINGLE_REQUEST_TIMEOUT,
                 wait_on_rate_limit=DEFAULT_WAIT_ON_RATE_LIMIT,
                 verify=DEFAULT_VERIFY,
                 version=None,
                 headers={'Content-type': 'application/json;charset=utf-8',
                          'Accept': 'application/json'},
                 debug=False,
                 uses_csrf_token=None,
                 get_csrf_token=None):
        """Initialize a new RestSession object.

        Args:
            get_access_token(callable): The Identity Services Engine method to get a new
                access token.
            access_token(basestring): The Identity Services Engine access token to be used
                for this session.
            base_url(basestring): The base URL that will be suffixed onto API
                endpoint relative URLs to produce a callable absolute URL.
            single_request_timeout(int): The timeout (seconds) for a single
                HTTP REST API request.
            wait_on_rate_limit(bool): Enable or disable automatic rate-limit
                handling.
            verify(bool,basestring): Controls whether we verify the server's
                TLS certificate, or a string, in which case it must be a path
                to a CA bundle to use.
            version(basestring): Controls which version of IDENTITY_SERVICES_ENGINE to use.
                Defaults to ciscoisesdk.config.IDENTITY_SERVICES_ENGINE_VERSION
            headers(dict): Allows to add headers to RestSession requests.
            debug(bool,basestring): Controls whether to log information about
                Identity Services Engine APIs' request and response process.
                Defaults to the DEBUG environment variable or False
                if the environment variable is not set.
            uses_csrf_token(bool): Controls whether we send the CSRF token to ISE's ERS APIs.
            get_csrf_token(callable):  The Identity Services Engine method to get a new
                CSRF token.

        Raises:
            TypeError: If the parameter types are incorrect.

        """
        check_type(access_token, basestring, may_be_none=False)
        check_type(base_url, basestring, may_be_none=False)
        check_type(single_request_timeout, int)
        check_type(wait_on_rate_limit, bool, may_be_none=False)
        check_type(verify, (bool, basestring), may_be_none=False)
        check_type(version, basestring, may_be_none=False)
        check_type(debug, (bool), may_be_none=False)
        check_type(uses_csrf_token, (bool), may_be_none=False)

        super(RestSession, self).__init__()

        # Initialize attributes and properties
        self._base_url = str(validate_base_url(base_url))
        self._get_access_token = get_access_token
        self._get_csrf_token = get_csrf_token
        self._csrf_token = None
        self._uses_csrf_token = uses_csrf_token
        self._access_token = str(access_token)
        self._single_request_timeout = single_request_timeout
        self._wait_on_rate_limit = wait_on_rate_limit
        self._verify = verify
        self._version = version
        self._debug = debug

        if self._debug:
            logger.setLevel(logging.DEBUG)
            logger.propagate = True
        else:
            logger.setLevel(logging.INFO)

        if verify is False:
            requests.packages.urllib3.disable_warnings()

        # Initialize a new `requests` session
        self._req_session = requests.session()

        # Update the headers of the `requests` session
        self.update_headers({'authorization': 'Basic ' + access_token})
        if headers and isinstance(headers, dict):
            self.update_headers(headers)

    @property
    def version(self):
        """The API version of Identity Services Engine."""
        return self._version

    @property
    def verify(self):
        """The verify (TLS Certificate) for the API endpoints."""
        return self._verify

    @verify.setter
    def verify(self, value):
        """The verify (TLS Certificate) for the API endpoints."""
        check_type(value, (bool, basestring), may_be_none=False)
        self._verify = value

    @property
    def base_url(self):
        """The base URL for the API endpoints."""
        return self._base_url

    @base_url.setter
    def base_url(self, value):
        """The base URL for the API endpoints."""
        check_type(value, basestring, may_be_none=False)
        self._base_url = str(validate_base_url(value))

    @property
    def single_request_timeout(self):
        """The timeout (seconds) for a single HTTP REST API request."""
        return self._single_request_timeout

    @single_request_timeout.setter
    def single_request_timeout(self, value):
        """The timeout (seconds) for a single HTTP REST API request."""
        check_type(value, int)
        assert value is None or value > 0
        self._single_request_timeout = value

    @property
    def wait_on_rate_limit(self):
        """Automatic rate-limit handling.

        This setting enables or disables automatic rate-limit handling.  When
        enabled, rate-limited requests will be automatically be retried after
        waiting `Retry-After` seconds (provided by Identity Services Engine in the
        rate-limit response header).

        """
        return self._wait_on_rate_limit

    @wait_on_rate_limit.setter
    def wait_on_rate_limit(self, value):
        """Enable or disable automatic rate-limit handling."""
        check_type(value, bool, may_be_none=False)
        self._wait_on_rate_limit = value

    @property
    def headers(self):
        """The HTTP headers used for requests in this session."""
        return self._req_session.headers.copy()

    @property
    def debug(self):
        """If log information about this REST session of the Identity Services Engine API's request and response process is shown."""
        return self._debug

    @debug.setter
    def debug(self, value):
        """If log information about this REST session of the Identity Services Engine API's request and response process is shown."""
        self._debug = value
        if self._debug:
            logger.setLevel(logging.DEBUG)
            logger.propagate = True
        else:
            logger.setLevel(logging.INFO)

    @property
    def uses_csrf_token(self):
        """If this RestSession requires the X-CSRF-Token to be sent."""
        return self._uses_csrf_token

    @uses_csrf_token.setter
    def uses_csrf_token(self, value):
        """If this RestSession requires the X-CSRF-Token to be sent."""
        check_type(value, (bool, basestring), may_be_none=False)
        self._uses_csrf_token = value
        if isinstance(self._uses_csrf_token, str):
            self._uses_csrf_token = 'true' in self._uses_csrf_token.lower()

    def update_headers(self, headers):
        """Update the HTTP headers used for requests in this session.

        Note: Updates provided by the dictionary passed as the `headers`
        parameter to this method are merged into the session headers by adding
        new key-value pairs and/or updating the values of existing keys. The
        session headers are not replaced by the provided dictionary.

        Args:
             headers(dict): Updates to the current session headers.

        """
        check_type(headers, dict, may_be_none=False)
        self._req_session.headers.update(headers)

    def refresh_token(self):
        """Call the get_access_token method and update the session's
        auth header with the new token.
        """
        self._access_token = self._get_access_token()
        self.update_headers({'authorization': 'Basic {}'.format(self._access_token)})

    def set_csrf_token(self):
        """Call the get_csrf_token method and update the session's
        X-CSRF-Token header with the new token.
        """
        if self._get_csrf_token is not None and callable(self._get_csrf_token):
            if self._csrf_token is None and self._uses_csrf_token:
                logger.debug('Refreshing CSRF token')
                self._csrf_token = self._get_csrf_token()
                logger.debug('Refreshed CSRF token.')
                self.update_headers({'X-CSRF-Token': self._csrf_token})

    def reset_csrf_token(self):
        self._csrf_token = None

    def abs_url(self, url):
        """Given a relative or absolute URL; return an absolute URL.

        Args:
            url(basestring): A relative or absolute URL.

        Returns:
            str: An absolute URL.

        """
        parsed_url = urllib.parse.urlparse(url)
        if not parsed_url.scheme and not parsed_url.netloc:
            # url is a relative URL; combine with base_url
            return urllib.parse.urljoin(str(self.base_url), str(url))
        else:
            # url is already an absolute URL; return as is
            return url

    def get_filename(self, content):
        """Get the filename from the Content-Disposition's header

        Args:
            content(basestring): the Content-Disposition's header

        Returns:
            str: the filename from the Content-Disposition's header

        Raises:
            Exception: If was not able to find the header's filename value.
        """
        content_file_list = re.findall('filename=(.*)', content)
        if len(content_file_list) > 0:
            content_file_name = content_file_list[0].replace('"', '')
        else:
            raise Exception("Could not find the header's filename value")
        return content_file_name

    def download(self, method, url, erc, custom_refresh, **kwargs):
        """It immediately downloads the response content.

        Args:
            method(basestring): The request-method type ('GET', 'POST', etc.).
            url(basestring): The URL of the API endpoint to be called.
            erc(int): The expected response code that should be returned by the
                Identity Services Engine API endpoint to indicate success.
            **kwargs: Passed on to the requests package.

        To download it to a file use the `save_file` kwarg equal to True.
        It defaults to False. If False is only 'downloaded' to a data property.

        To specify the downloaded file use the `filename` kwarg.
        It defaults to the value of the Content-Disposition header's filename.

        To specify the downloaded directory path use the `dirpath` kwarg.
        It defaults to the os.getcwd() result.

        Returns:
            DownloadResponse: The DownloadResponse wrapper. Wraps the urllib3.response.HTTPResponse. For more
            information check the `urlib3 documentation <https://urllib3.readthedocs.io/en/latest/reference/urllib3.response.html>`_

        Raises:
            DownloadFailure: If was not able to download the raw
            response to a file.
        """
        save_file = kwargs.pop('save_file', False)
        dirpath = kwargs.pop('dirpath', None)
        filename = kwargs.pop('filename', None)
        filepath = None
        collected_data = bytes()

        if not(dirpath) or not(os.path.isdir(dirpath)):
            dirpath = os.getcwd()

        with self.request(method, url, erc, 0, **kwargs) as resp:
            if resp.headers and resp.headers.get('Content-Disposition'):
                try:
                    content = resp.headers.get('Content-Disposition')
                    filename = filename or self.get_filename(content)
                    filepath = os.path.join(dirpath, filename)
                except Exception as e:
                    raise DownloadFailure(resp, e)
            if save_file and filepath:
                try:
                    with open(filepath, 'wb') as f:
                        logger.debug('Downloading {0}'.format(filepath))
                        for chunk in resp.iter_content(chunk_size=1024):
                            if chunk:
                                collected_data += chunk
                                f.write(chunk)
                except Exception as e:
                    raise DownloadFailure(resp, e)
                logger.debug('Downloaded {0}'.format(filepath))
            final_response = DownloadResponse(resp, filepath, filename, dirpath, collected_data)
            return final_response

    def request(self, method, url, erc, custom_refresh, **kwargs):
        """Abstract base method for making requests to the Identity Services Engine APIs.

        This base method:
            * Expands the API endpoint URL to an absolute URL
            * Makes the actual HTTP request to the API endpoint
            * Provides support for Identity Services Engine rate-limiting
            * Inspects response codes and raises exceptions as appropriate
            * Updates the token if response code is 401 - Unauthorized
                and makes the request to the API endpoint again

        Args:
            method(basestring): The request-method type ('GET', 'POST', etc.).
            url(basestring): The URL of the API endpoint to be called.
            erc(int): The expected response code that should be returned by the
                Identity Services Engine API endpoint to indicate success.
            **kwargs: Passed on to the requests package.

        Returns:
            requests.Response: The Response object, which contains a server's response to an HTTP request.

        Raises:
            ApiError: If anything other than the expected response code is
                returned by the Identity Services Engine API endpoint.

        """
        # Ensure the url is an absolute URL
        abs_url = self.abs_url(url)

        # Update request kwargs with session defaults
        kwargs.setdefault('timeout', self.single_request_timeout)
        kwargs.setdefault('verify', self.verify)

        # Fixes requests inconsistent behavior with additional parameters
        if not kwargs.get('json'):
            kwargs.pop('json', None)

        if not kwargs.get('data'):
            kwargs.pop('data', None)

        requires_csrf = method in ['POST', 'PUT', 'DELETE']
        if requires_csrf:
            self.set_csrf_token()

        c = custom_refresh
        while True:
            c += 1
            # Make the HTTP request to the API endpoint
            try:
                logger.debug('Attempt {}'.format(c))
                logger.debug(pprint_request_info(abs_url, method,
                                                 _headers=self.headers,
                                                 **kwargs))
                response = self._req_session.request(method, abs_url, **kwargs)
            except socket.error:
                # A socket error
                self.reset_csrf_token()
                try:
                    c += 1
                    logger.debug('Attempt {}'.format(c))
                    response = self._req_session.request(method, abs_url,
                                                         **kwargs)
                except Exception as e:
                    raise ciscoisesdkException('Socket error {}'.format(e))
            except IOError as e:
                self.reset_csrf_token()
                if e.errno == errno.EPIPE:
                    # EPIPE error
                    try:
                        c += 1
                        logger.debug('Attempt {}'.format(c))
                        response = self._req_session.request(method, abs_url,
                                                             **kwargs)
                    except Exception as e:
                        raise ciscoisesdkException('PipeError {}'.format(e))
                else:
                    raise ciscoisesdkException('IOError {}'.format(e))
            try:
                # Check the response code for error conditions
                check_response_code(response, erc,
                                    additional_data=get_exception_additional_data(headers=self.headers, response=response))
            except RateLimitError as e:
                self.reset_csrf_token()
                # Catch rate-limit errors
                # Wait and retry if automatic rate-limit handling is enabled
                if self.wait_on_rate_limit:
                    warnings.warn(RateLimitWarning(response))
                    time.sleep(e.retry_after)
                    continue
                else:
                    # Re-raise the RateLimitError
                    raise
            except ApiError as e:
                self.reset_csrf_token()
                if e.status_code == 401 and custom_refresh < 1:
                    logger.debug(pprint_response_info(response))
                    logger.debug('Refreshing access token')
                    self.refresh_token()
                    logger.debug('Refreshed token.')
                    return self.request(method, url, erc, 1, **kwargs)
                elif e.status_code == 403 and custom_refresh < 1:
                    logger.debug(pprint_response_info(response))
                    return self.request(method, url, erc, 1, **kwargs)
                else:
                    # Re-raise the ApiError
                    logger.debug(pprint_response_info(response))
                    raise
            else:
                logger.debug(pprint_response_info(response))
                return response

    def multipart_data(self, fields, create_callback):
        """Creates a multipart/form-data body.

        Args:
            fields(dict,list): form data values.
            create_callback(function): function that creates a function that
                monitors the progress of the upload.
            boundary: MultipartEncoder's boundary.
                Default value: None.
            encoding(string): MultipartEncoder's encoding.
                Default value: utf-8.
        """
        if fields is not None:
            e = encoder.MultipartEncoder(
                fields=fields
            )
            if create_callback is not None:
                callback = create_callback(e)
                m = encoder.MultipartEncoderMonitor(e, callback)
                return m
            else:
                return e
        else:
            return None

    def get(self, url, params=None, **kwargs):
        """Sends a GET request.

        Args:
            url(basestring): The URL of the API endpoint.
            params(dict): The parameters for the HTTP GET request.
            **kwargs:
                erc(int): The expected (success) response code for the request.
                others: Passed on to the requests package.

        Returns:
            DownloadResponse: If it has `stream` kwarg with a True value.
            Any: Result of the `json.loads` of the server's response to an HTTP request.

        Raises:
            ApiError: If anything other than the expected response code is
                returned by the Identity Services Engine API endpoint.

        """
        check_type(url, basestring, may_be_none=False)
        check_type(params, dict)

        # Expected response code
        erc = kwargs.pop('erc', EXPECTED_RESPONSE_CODE['GET'])

        stream = kwargs.get('stream', None)
        if stream:
            return self.download('GET', url, erc, 0, params=params, **kwargs)
        else:
            response = self.request('GET', url, erc, 0, params=params, **kwargs)
            return RestResponse(response)

    def post(self, url, params=None, json=None, data=None, **kwargs):
        """Sends a POST request.

        Args:
            url(basestring): The URL of the API endpoint.
            json: Data to be sent in JSON format in tbe body of the request.
            data: Data to be sent in the body of the request.
            **kwargs:
                erc(int): The expected (success) response code for the request.
                others: Passed on to the requests package.

        Returns:
            DownloadResponse: If it has `stream` kwarg with a True value.
            Any: Result of the `json.loads` of the server's response to an HTTP request.

        Raises:
            ApiError: If anything other than the expected response code is
                returned by the Identity Services Engine API endpoint.

        """
        check_type(url, basestring, may_be_none=False)
        check_type(params, dict)

        # Expected response code
        erc = kwargs.pop('erc', EXPECTED_RESPONSE_CODE['POST'])

        stream = kwargs.get('stream', None)
        if stream:
            return self.download('POST', url, erc, 0, params=params,
                                 json=json, data=data, **kwargs)
        else:
            response = self.request('POST', url, erc, 0, params=params,
                                    json=json, data=data, **kwargs)
            return RestResponse(response)

    def put(self, url, params=None, json=None, data=None, **kwargs):
        """Sends a PUT request.

        Args:
            url(basestring): The URL of the API endpoint.
            json: Data to be sent in JSON format in tbe body of the request.
            data: Data to be sent in the body of the request.
            **kwargs:
                erc(int): The expected (success) response code for the request.
                others: Passed on to the requests package.

        Returns:
            DownloadResponse: If it has `stream` kwarg with a True value.
            Any: Result of the `json.loads` of the server's response to an HTTP request.

        Raises:
            ApiError: If anything other than the expected response code is
                returned by the Identity Services Engine API endpoint.

        """
        check_type(url, basestring, may_be_none=False)
        check_type(params, dict)

        # Expected response code
        erc = kwargs.pop('erc', EXPECTED_RESPONSE_CODE['PUT'])

        stream = kwargs.get('stream', None)
        if stream:
            return self.download('PUT', url, erc, 0, params=params,
                                 json=json, data=data, **kwargs)
        else:
            response = self.request('PUT', url, erc, 0, params=params,
                                    json=json, data=data, **kwargs)
            return RestResponse(response)

    def delete(self, url, params=None, **kwargs):
        """Sends a DELETE request.

        Args:
            url(basestring): The URL of the API endpoint.
            **kwargs:
                erc(int): The expected (success) response code for the request.
                others: Passed on to the requests package.

        Raises:
            ApiError: If anything other than the expected response code is
                returned by the Identity Services Engine API endpoint.

        """
        check_type(url, basestring, may_be_none=False)
        check_type(params, dict)

        # Expected response code
        erc = kwargs.pop('erc', EXPECTED_RESPONSE_CODE['DELETE'])

        response = self.request('DELETE', url, erc, 0, params=params, **kwargs)
        return RestResponse(response)
