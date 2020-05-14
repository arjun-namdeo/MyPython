#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Custom exception which could generate Grab instance.

Taxonomy:

Exception
|-> GrabError
    |-> GrabNetworkError <- IOError
    |-> DataNotFound <- IndexError
    |-> Grab*Error

"""
import warnings


class GrabError(Exception):
    """
    All custom Grab exception should be children of that class.
    """
    pass


class GrabNetworkError(IOError, GrabError):
    """
    Raises in case of network error.
    """
    pass


class GrabTimeoutError(GrabNetworkError):
    """
    Raises when configured time is outed for the request.

    In curl transport it is CURLE_OPERATION_TIMEDOUT (28)
    """
    pass


class DataNotFound(IndexError, GrabError):
    """
    Indictes that required data is not found.
    """
    pass


class GrabMisuseError(GrabError):
    """
    Indicates incorrect usage of grab API.
    """
    pass


class GrabConnectionError(GrabNetworkError):
    """
    Raised when it is not possible to establish network connection.

    In curl transport it is CURLE_COULDNT_CONNECT (7)
    """
    pass


class GrabAuthError(GrabError):
    """
    Raised when remote server denies authentication credentials.

    In curl transport it is CURLE_COULDNT_CONNECT (67)
    """
    pass


class GrabTooManyRedirectsError(GrabError):
    """
    Raised when Grab reached max. allowd number of redirects for
    one request.
    """
    pass


class GrabDeprecationWarning(Warning):
    """
    Raised when some deprecated feature is used.
    """
    pass


class GrabInvalidUrl(GrabError):
    """
    Raised when Grab have no idea how to handle the URL or when
    some error occured while normalizing URL e.g. IDN processing.
    """
    pass


def warn(msg):
    warnings.warn(msg, category=GrabDeprecationWarning, stacklevel=3)
