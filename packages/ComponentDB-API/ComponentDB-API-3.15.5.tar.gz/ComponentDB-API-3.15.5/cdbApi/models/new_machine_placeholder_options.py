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


class NewMachinePlaceholderOptions(object):
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
        'alternate_name': 'str',
        'description': 'str',
        'project_id': 'int'
    }

    attribute_map = {
        'name': 'name',
        'alternate_name': 'alternateName',
        'description': 'description',
        'project_id': 'projectId'
    }

    def __init__(self, name=None, alternate_name=None, description=None, project_id=None, local_vars_configuration=None):  # noqa: E501
        """NewMachinePlaceholderOptions - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._alternate_name = None
        self._description = None
        self._project_id = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if alternate_name is not None:
            self.alternate_name = alternate_name
        if description is not None:
            self.description = description
        if project_id is not None:
            self.project_id = project_id

    @property
    def name(self):
        """Gets the name of this NewMachinePlaceholderOptions.  # noqa: E501


        :return: The name of this NewMachinePlaceholderOptions.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this NewMachinePlaceholderOptions.


        :param name: The name of this NewMachinePlaceholderOptions.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def alternate_name(self):
        """Gets the alternate_name of this NewMachinePlaceholderOptions.  # noqa: E501


        :return: The alternate_name of this NewMachinePlaceholderOptions.  # noqa: E501
        :rtype: str
        """
        return self._alternate_name

    @alternate_name.setter
    def alternate_name(self, alternate_name):
        """Sets the alternate_name of this NewMachinePlaceholderOptions.


        :param alternate_name: The alternate_name of this NewMachinePlaceholderOptions.  # noqa: E501
        :type: str
        """

        self._alternate_name = alternate_name

    @property
    def description(self):
        """Gets the description of this NewMachinePlaceholderOptions.  # noqa: E501


        :return: The description of this NewMachinePlaceholderOptions.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this NewMachinePlaceholderOptions.


        :param description: The description of this NewMachinePlaceholderOptions.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def project_id(self):
        """Gets the project_id of this NewMachinePlaceholderOptions.  # noqa: E501


        :return: The project_id of this NewMachinePlaceholderOptions.  # noqa: E501
        :rtype: int
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        """Sets the project_id of this NewMachinePlaceholderOptions.


        :param project_id: The project_id of this NewMachinePlaceholderOptions.  # noqa: E501
        :type: int
        """

        self._project_id = project_id

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
        if not isinstance(other, NewMachinePlaceholderOptions):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, NewMachinePlaceholderOptions):
            return True

        return self.to_dict() != other.to_dict()
