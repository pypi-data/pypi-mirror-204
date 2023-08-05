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


class NewAppInformation(object):
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
        'name': 'str',
        'description': 'str',
        'technical_system_list': 'list[ItemCategory]',
        'type_list': 'list[ItemType]'
    }

    attribute_map = {
        'name': 'name',
        'description': 'description',
        'technical_system_list': 'technicalSystemList',
        'type_list': 'typeList'
    }

    def __init__(self, name=None, description=None, technical_system_list=None, type_list=None, local_vars_configuration=None):  # noqa: E501
        """NewAppInformation - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._description = None
        self._technical_system_list = None
        self._type_list = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if technical_system_list is not None:
            self.technical_system_list = technical_system_list
        if type_list is not None:
            self.type_list = type_list

    @property
    def name(self):
        """Gets the name of this NewAppInformation.  # noqa: E501


        :return: The name of this NewAppInformation.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this NewAppInformation.


        :param name: The name of this NewAppInformation.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def description(self):
        """Gets the description of this NewAppInformation.  # noqa: E501


        :return: The description of this NewAppInformation.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this NewAppInformation.


        :param description: The description of this NewAppInformation.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def technical_system_list(self):
        """Gets the technical_system_list of this NewAppInformation.  # noqa: E501


        :return: The technical_system_list of this NewAppInformation.  # noqa: E501
        :rtype: list[ItemCategory]
        """
        return self._technical_system_list

    @technical_system_list.setter
    def technical_system_list(self, technical_system_list):
        """Sets the technical_system_list of this NewAppInformation.


        :param technical_system_list: The technical_system_list of this NewAppInformation.  # noqa: E501
        :type: list[ItemCategory]
        """

        self._technical_system_list = technical_system_list

    @property
    def type_list(self):
        """Gets the type_list of this NewAppInformation.  # noqa: E501


        :return: The type_list of this NewAppInformation.  # noqa: E501
        :rtype: list[ItemType]
        """
        return self._type_list

    @type_list.setter
    def type_list(self, type_list):
        """Sets the type_list of this NewAppInformation.


        :param type_list: The type_list of this NewAppInformation.  # noqa: E501
        :type: list[ItemType]
        """

        self._type_list = type_list

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
        if not isinstance(other, NewAppInformation):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, NewAppInformation):
            return True

        return self.to_dict() != other.to_dict()
