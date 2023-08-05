# coding: utf-8

"""
    Component Database API

    The API that provides access to Component Database data.  # noqa: E501

    The version of the OpenAPI document: 3.15.5
    Contact: djarosz@anl.gov
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from cdbApi.configuration import Configuration


class ApiExceptionMessage(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'simple_name': 'str',
        'message': 'str',
        'exception': 'ApiExceptionMessageException'
    }

    attribute_map = {
        'simple_name': 'simpleName',
        'message': 'message',
        'exception': 'exception'
    }

    def __init__(self, simple_name=None, message=None, exception=None, local_vars_configuration=None):  # noqa: E501
        """ApiExceptionMessage - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._simple_name = None
        self._message = None
        self._exception = None
        self.discriminator = None

        if simple_name is not None:
            self.simple_name = simple_name
        if message is not None:
            self.message = message
        if exception is not None:
            self.exception = exception

    @property
    def simple_name(self):
        """Gets the simple_name of this ApiExceptionMessage.  # noqa: E501


        :return: The simple_name of this ApiExceptionMessage.  # noqa: E501
        :rtype: str
        """
        return self._simple_name

    @simple_name.setter
    def simple_name(self, simple_name):
        """Sets the simple_name of this ApiExceptionMessage.


        :param simple_name: The simple_name of this ApiExceptionMessage.  # noqa: E501
        :type: str
        """

        self._simple_name = simple_name

    @property
    def message(self):
        """Gets the message of this ApiExceptionMessage.  # noqa: E501


        :return: The message of this ApiExceptionMessage.  # noqa: E501
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this ApiExceptionMessage.


        :param message: The message of this ApiExceptionMessage.  # noqa: E501
        :type: str
        """

        self._message = message

    @property
    def exception(self):
        """Gets the exception of this ApiExceptionMessage.  # noqa: E501


        :return: The exception of this ApiExceptionMessage.  # noqa: E501
        :rtype: ApiExceptionMessageException
        """
        return self._exception

    @exception.setter
    def exception(self, exception):
        """Sets the exception of this ApiExceptionMessage.


        :param exception: The exception of this ApiExceptionMessage.  # noqa: E501
        :type: ApiExceptionMessageException
        """

        self._exception = exception

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ApiExceptionMessage):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ApiExceptionMessage):
            return True

        return self.to_dict() != other.to_dict()
