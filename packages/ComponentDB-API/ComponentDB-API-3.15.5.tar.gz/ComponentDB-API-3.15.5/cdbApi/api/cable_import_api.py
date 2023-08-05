# coding: utf-8

"""
    Component Database API

    The API that provides access to Component Database data.  # noqa: E501

    The version of the OpenAPI document: 3.15.5
    Contact: djarosz@anl.gov
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from cdbApi.api_client import ApiClient
from cdbApi.exceptions import (  # noqa: F401
    ApiTypeError,
    ApiValueError
)


class CableImportApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def get_cable_catalog_info_list(self, item_domain_cable_catalog_id_list_request, **kwargs):  # noqa: E501
        """get_cable_catalog_info_list  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_cable_catalog_info_list(item_domain_cable_catalog_id_list_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param ItemDomainCableCatalogIdListRequest item_domain_cable_catalog_id_list_request: (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: list[CableCatalogItemInfo]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.get_cable_catalog_info_list_with_http_info(item_domain_cable_catalog_id_list_request, **kwargs)  # noqa: E501

    def get_cable_catalog_info_list_with_http_info(self, item_domain_cable_catalog_id_list_request, **kwargs):  # noqa: E501
        """get_cable_catalog_info_list  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_cable_catalog_info_list_with_http_info(item_domain_cable_catalog_id_list_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param ItemDomainCableCatalogIdListRequest item_domain_cable_catalog_id_list_request: (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(list[CableCatalogItemInfo], status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = [
            'item_domain_cable_catalog_id_list_request'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_cable_catalog_info_list" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'item_domain_cable_catalog_id_list_request' is set
        if self.api_client.client_side_validation and ('item_domain_cable_catalog_id_list_request' not in local_var_params or  # noqa: E501
                                                        local_var_params['item_domain_cable_catalog_id_list_request'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `item_domain_cable_catalog_id_list_request` when calling `get_cable_catalog_info_list`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'item_domain_cable_catalog_id_list_request' in local_var_params:
            body_params = local_var_params['item_domain_cable_catalog_id_list_request']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/api/CableImport/CableCatalogInfoList', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[CableCatalogItemInfo]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_cable_type_id_list(self, item_domain_cable_catalog_id_list_request, **kwargs):  # noqa: E501
        """get_cable_type_id_list  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_cable_type_id_list(item_domain_cable_catalog_id_list_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param ItemDomainCableCatalogIdListRequest item_domain_cable_catalog_id_list_request: (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: list[int]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.get_cable_type_id_list_with_http_info(item_domain_cable_catalog_id_list_request, **kwargs)  # noqa: E501

    def get_cable_type_id_list_with_http_info(self, item_domain_cable_catalog_id_list_request, **kwargs):  # noqa: E501
        """get_cable_type_id_list  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_cable_type_id_list_with_http_info(item_domain_cable_catalog_id_list_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param ItemDomainCableCatalogIdListRequest item_domain_cable_catalog_id_list_request: (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(list[int], status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = [
            'item_domain_cable_catalog_id_list_request'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_cable_type_id_list" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'item_domain_cable_catalog_id_list_request' is set
        if self.api_client.client_side_validation and ('item_domain_cable_catalog_id_list_request' not in local_var_params or  # noqa: E501
                                                        local_var_params['item_domain_cable_catalog_id_list_request'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `item_domain_cable_catalog_id_list_request` when calling `get_cable_type_id_list`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'item_domain_cable_catalog_id_list_request' in local_var_params:
            body_params = local_var_params['item_domain_cable_catalog_id_list_request']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/api/CableImport/CableCatalogIdList', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[int]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_machine_info_list(self, item_domain_machine_design_id_list_request, **kwargs):  # noqa: E501
        """get_machine_info_list  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_machine_info_list(item_domain_machine_design_id_list_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param ItemDomainMachineDesignIdListRequest item_domain_machine_design_id_list_request: (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: list[MachineDesignItemInfo]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.get_machine_info_list_with_http_info(item_domain_machine_design_id_list_request, **kwargs)  # noqa: E501

    def get_machine_info_list_with_http_info(self, item_domain_machine_design_id_list_request, **kwargs):  # noqa: E501
        """get_machine_info_list  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_machine_info_list_with_http_info(item_domain_machine_design_id_list_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param ItemDomainMachineDesignIdListRequest item_domain_machine_design_id_list_request: (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(list[MachineDesignItemInfo], status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = [
            'item_domain_machine_design_id_list_request'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_machine_info_list" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'item_domain_machine_design_id_list_request' is set
        if self.api_client.client_side_validation and ('item_domain_machine_design_id_list_request' not in local_var_params or  # noqa: E501
                                                        local_var_params['item_domain_machine_design_id_list_request'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `item_domain_machine_design_id_list_request` when calling `get_machine_info_list`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'item_domain_machine_design_id_list_request' in local_var_params:
            body_params = local_var_params['item_domain_machine_design_id_list_request']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/api/CableImport/MachineInfoList', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[MachineDesignItemInfo]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)
