# coding: utf-8

"""
    Assetic Integration API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: v2
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from assetic.api_client import ApiClient


class ResourceApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def resource_get(self, **kwargs):  # noqa: E501
        """Gets resources based on request parameters  # noqa: E501

        Status fields (Status and StatusId) only supports operators 'is equals to' and 'is not equals to' <br />  • Status field accepts Active and Inactive as value <br />  • StatusId field accepts 1 as Active and 2 as Inactive <br /><br /><br />  Sample request to get Active resources:<br /><pre>/api/v2/resource/?requestParams.filters=Status~eq~'Active'<br />/api/v2/resource/?requestParams.filters=StatusId~neq~2<br /></pre>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.resource_get(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param list[str] request_params_sorts:
        :param list[str] request_params_filters:
        :param int request_params_page:
        :param int request_params_page_size:
        :return: ResourceListRepresentation
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.resource_get_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.resource_get_with_http_info(**kwargs)  # noqa: E501
            return data

    def resource_get_with_http_info(self, **kwargs):  # noqa: E501
        """Gets resources based on request parameters  # noqa: E501

        Status fields (Status and StatusId) only supports operators 'is equals to' and 'is not equals to' <br />  • Status field accepts Active and Inactive as value <br />  • StatusId field accepts 1 as Active and 2 as Inactive <br /><br /><br />  Sample request to get Active resources:<br /><pre>/api/v2/resource/?requestParams.filters=Status~eq~'Active'<br />/api/v2/resource/?requestParams.filters=StatusId~neq~2<br /></pre>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.resource_get_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param list[str] request_params_sorts:
        :param list[str] request_params_filters:
        :param int request_params_page:
        :param int request_params_page_size:
        :return: ResourceListRepresentation
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['request_params_sorts', 'request_params_filters', 'request_params_page', 'request_params_page_size']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method resource_get" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'request_params_sorts' in params:
            query_params.append(('requestParams.sorts', params['request_params_sorts']))  # noqa: E501
            collection_formats['requestParams.sorts'] = 'multi'  # noqa: E501
        if 'request_params_filters' in params:
            query_params.append(('requestParams.filters', params['request_params_filters']))  # noqa: E501
            collection_formats['requestParams.filters'] = 'multi'  # noqa: E501
        if 'request_params_page' in params:
            query_params.append(('requestParams.page', params['request_params_page']))  # noqa: E501
        if 'request_params_page_size' in params:
            query_params.append(('requestParams.pageSize', params['request_params_page_size']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'text/json', 'application/octet-stream'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/api/v2/resource', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ResourceListRepresentation',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def resource_post(self, resource, **kwargs):  # noqa: E501
        """Create a new resource.  # noqa: E501

        • Status field accepts Active and Inactive as value <br />  • Resource Type will only take Type's name, which accepts Team, Customer, Contractor, Employee, Company and All as value. <br /><br /><br />  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.resource_post(resource, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ResourceRepresentation resource: (required)
        :return: CreatedRepresentationResourceRepresentation
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.resource_post_with_http_info(resource, **kwargs)  # noqa: E501
        else:
            (data) = self.resource_post_with_http_info(resource, **kwargs)  # noqa: E501
            return data

    def resource_post_with_http_info(self, resource, **kwargs):  # noqa: E501
        """Create a new resource.  # noqa: E501

        • Status field accepts Active and Inactive as value <br />  • Resource Type will only take Type's name, which accepts Team, Customer, Contractor, Employee, Company and All as value. <br /><br /><br />  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.resource_post_with_http_info(resource, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ResourceRepresentation resource: (required)
        :return: CreatedRepresentationResourceRepresentation
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['resource']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method resource_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'resource' is set
        if ('resource' not in params or
                params['resource'] is None):
            raise ValueError("Missing the required parameter `resource` when calling `resource_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'resource' in params:
            body_params = params['resource']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'text/json', 'application/octet-stream'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'text/json', 'application/octet-stream', 'application/x-www-form-urlencoded', 'application/hal+json', 'application/hal+xml'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/api/v2/resource', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='CreatedRepresentationResourceRepresentation',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def resource_put(self, id, resource, **kwargs):  # noqa: E501
        """Update resources details.  # noqa: E501

        • Status field accepts Active and Inactive as value <br />  • Resource Type will only take Type's name instead of type ID. <br /><br /><br />  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.resource_put(id, resource, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: Id For resource. (required)
        :param ResourceRepresentation resource: (required)
        :return: ResourceRepresentation
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.resource_put_with_http_info(id, resource, **kwargs)  # noqa: E501
        else:
            (data) = self.resource_put_with_http_info(id, resource, **kwargs)  # noqa: E501
            return data

    def resource_put_with_http_info(self, id, resource, **kwargs):  # noqa: E501
        """Update resources details.  # noqa: E501

        • Status field accepts Active and Inactive as value <br />  • Resource Type will only take Type's name instead of type ID. <br /><br /><br />  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.resource_put_with_http_info(id, resource, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: Id For resource. (required)
        :param ResourceRepresentation resource: (required)
        :return: ResourceRepresentation
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['id', 'resource']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method resource_put" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `resource_put`")  # noqa: E501
        # verify the required parameter 'resource' is set
        if ('resource' not in params or
                params['resource'] is None):
            raise ValueError("Missing the required parameter `resource` when calling `resource_put`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'resource' in params:
            body_params = params['resource']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'text/json', 'application/octet-stream'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'text/json', 'application/octet-stream', 'application/x-www-form-urlencoded', 'application/hal+json', 'application/hal+xml'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/api/v2/resource/{id}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ResourceRepresentation',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
