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


class ItemDomainMachineDesignIdListRequest(object):
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
        'item_names': 'list[str]',
        'rack_names': 'list[str]',
        'root_name': 'str'
    }

    attribute_map = {
        'item_names': 'itemNames',
        'rack_names': 'rackNames',
        'root_name': 'rootName'
    }

    def __init__(self, item_names=None, rack_names=None, root_name=None, local_vars_configuration=None):  # noqa: E501
        """ItemDomainMachineDesignIdListRequest - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._item_names = None
        self._rack_names = None
        self._root_name = None
        self.discriminator = None

        if item_names is not None:
            self.item_names = item_names
        if rack_names is not None:
            self.rack_names = rack_names
        if root_name is not None:
            self.root_name = root_name

    @property
    def item_names(self):
        """Gets the item_names of this ItemDomainMachineDesignIdListRequest.  # noqa: E501


        :return: The item_names of this ItemDomainMachineDesignIdListRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._item_names

    @item_names.setter
    def item_names(self, item_names):
        """Sets the item_names of this ItemDomainMachineDesignIdListRequest.


        :param item_names: The item_names of this ItemDomainMachineDesignIdListRequest.  # noqa: E501
        :type: list[str]
        """

        self._item_names = item_names

    @property
    def rack_names(self):
        """Gets the rack_names of this ItemDomainMachineDesignIdListRequest.  # noqa: E501


        :return: The rack_names of this ItemDomainMachineDesignIdListRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._rack_names

    @rack_names.setter
    def rack_names(self, rack_names):
        """Sets the rack_names of this ItemDomainMachineDesignIdListRequest.


        :param rack_names: The rack_names of this ItemDomainMachineDesignIdListRequest.  # noqa: E501
        :type: list[str]
        """

        self._rack_names = rack_names

    @property
    def root_name(self):
        """Gets the root_name of this ItemDomainMachineDesignIdListRequest.  # noqa: E501


        :return: The root_name of this ItemDomainMachineDesignIdListRequest.  # noqa: E501
        :rtype: str
        """
        return self._root_name

    @root_name.setter
    def root_name(self, root_name):
        """Sets the root_name of this ItemDomainMachineDesignIdListRequest.


        :param root_name: The root_name of this ItemDomainMachineDesignIdListRequest.  # noqa: E501
        :type: str
        """

        self._root_name = root_name

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
        if not isinstance(other, ItemDomainMachineDesignIdListRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ItemDomainMachineDesignIdListRequest):
            return True

        return self.to_dict() != other.to_dict()
