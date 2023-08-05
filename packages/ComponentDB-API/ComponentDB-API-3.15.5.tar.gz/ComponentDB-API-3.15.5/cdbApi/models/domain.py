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


class Domain(object):
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
        'id': 'int',
        'name': 'str',
        'description': 'str',
        'item_identifier1_label': 'str',
        'item_identifier2_label': 'str',
        'item_type_label': 'str',
        'item_category_label': 'str',
        'item_list': 'list[Item]',
        'property_type_list': 'list[PropertyType]',
        'item_type_list': 'list[ItemType]',
        'item_category_list': 'list[ItemCategory]',
        'allowed_entity_type_list': 'list[EntityType]',
        'domain_rep_icon': 'str'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'description': 'description',
        'item_identifier1_label': 'itemIdentifier1Label',
        'item_identifier2_label': 'itemIdentifier2Label',
        'item_type_label': 'itemTypeLabel',
        'item_category_label': 'itemCategoryLabel',
        'item_list': 'itemList',
        'property_type_list': 'propertyTypeList',
        'item_type_list': 'itemTypeList',
        'item_category_list': 'itemCategoryList',
        'allowed_entity_type_list': 'allowedEntityTypeList',
        'domain_rep_icon': 'domainRepIcon'
    }

    def __init__(self, id=None, name=None, description=None, item_identifier1_label=None, item_identifier2_label=None, item_type_label=None, item_category_label=None, item_list=None, property_type_list=None, item_type_list=None, item_category_list=None, allowed_entity_type_list=None, domain_rep_icon=None, local_vars_configuration=None):  # noqa: E501
        """Domain - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._name = None
        self._description = None
        self._item_identifier1_label = None
        self._item_identifier2_label = None
        self._item_type_label = None
        self._item_category_label = None
        self._item_list = None
        self._property_type_list = None
        self._item_type_list = None
        self._item_category_list = None
        self._allowed_entity_type_list = None
        self._domain_rep_icon = None
        self.discriminator = None

        if id is not None:
            self.id = id
        self.name = name
        if description is not None:
            self.description = description
        if item_identifier1_label is not None:
            self.item_identifier1_label = item_identifier1_label
        if item_identifier2_label is not None:
            self.item_identifier2_label = item_identifier2_label
        if item_type_label is not None:
            self.item_type_label = item_type_label
        if item_category_label is not None:
            self.item_category_label = item_category_label
        if item_list is not None:
            self.item_list = item_list
        if property_type_list is not None:
            self.property_type_list = property_type_list
        if item_type_list is not None:
            self.item_type_list = item_type_list
        if item_category_list is not None:
            self.item_category_list = item_category_list
        if allowed_entity_type_list is not None:
            self.allowed_entity_type_list = allowed_entity_type_list
        if domain_rep_icon is not None:
            self.domain_rep_icon = domain_rep_icon

    @property
    def id(self):
        """Gets the id of this Domain.  # noqa: E501


        :return: The id of this Domain.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Domain.


        :param id: The id of this Domain.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this Domain.  # noqa: E501


        :return: The name of this Domain.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Domain.


        :param name: The name of this Domain.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                name is not None and len(name) > 64):
            raise ValueError("Invalid value for `name`, length must be less than or equal to `64`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                name is not None and len(name) < 1):
            raise ValueError("Invalid value for `name`, length must be greater than or equal to `1`")  # noqa: E501

        self._name = name

    @property
    def description(self):
        """Gets the description of this Domain.  # noqa: E501


        :return: The description of this Domain.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this Domain.


        :param description: The description of this Domain.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                description is not None and len(description) > 256):
            raise ValueError("Invalid value for `description`, length must be less than or equal to `256`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                description is not None and len(description) < 0):
            raise ValueError("Invalid value for `description`, length must be greater than or equal to `0`")  # noqa: E501

        self._description = description

    @property
    def item_identifier1_label(self):
        """Gets the item_identifier1_label of this Domain.  # noqa: E501


        :return: The item_identifier1_label of this Domain.  # noqa: E501
        :rtype: str
        """
        return self._item_identifier1_label

    @item_identifier1_label.setter
    def item_identifier1_label(self, item_identifier1_label):
        """Sets the item_identifier1_label of this Domain.


        :param item_identifier1_label: The item_identifier1_label of this Domain.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                item_identifier1_label is not None and len(item_identifier1_label) > 32):
            raise ValueError("Invalid value for `item_identifier1_label`, length must be less than or equal to `32`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                item_identifier1_label is not None and len(item_identifier1_label) < 0):
            raise ValueError("Invalid value for `item_identifier1_label`, length must be greater than or equal to `0`")  # noqa: E501

        self._item_identifier1_label = item_identifier1_label

    @property
    def item_identifier2_label(self):
        """Gets the item_identifier2_label of this Domain.  # noqa: E501


        :return: The item_identifier2_label of this Domain.  # noqa: E501
        :rtype: str
        """
        return self._item_identifier2_label

    @item_identifier2_label.setter
    def item_identifier2_label(self, item_identifier2_label):
        """Sets the item_identifier2_label of this Domain.


        :param item_identifier2_label: The item_identifier2_label of this Domain.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                item_identifier2_label is not None and len(item_identifier2_label) > 32):
            raise ValueError("Invalid value for `item_identifier2_label`, length must be less than or equal to `32`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                item_identifier2_label is not None and len(item_identifier2_label) < 0):
            raise ValueError("Invalid value for `item_identifier2_label`, length must be greater than or equal to `0`")  # noqa: E501

        self._item_identifier2_label = item_identifier2_label

    @property
    def item_type_label(self):
        """Gets the item_type_label of this Domain.  # noqa: E501


        :return: The item_type_label of this Domain.  # noqa: E501
        :rtype: str
        """
        return self._item_type_label

    @item_type_label.setter
    def item_type_label(self, item_type_label):
        """Sets the item_type_label of this Domain.


        :param item_type_label: The item_type_label of this Domain.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                item_type_label is not None and len(item_type_label) > 32):
            raise ValueError("Invalid value for `item_type_label`, length must be less than or equal to `32`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                item_type_label is not None and len(item_type_label) < 0):
            raise ValueError("Invalid value for `item_type_label`, length must be greater than or equal to `0`")  # noqa: E501

        self._item_type_label = item_type_label

    @property
    def item_category_label(self):
        """Gets the item_category_label of this Domain.  # noqa: E501


        :return: The item_category_label of this Domain.  # noqa: E501
        :rtype: str
        """
        return self._item_category_label

    @item_category_label.setter
    def item_category_label(self, item_category_label):
        """Sets the item_category_label of this Domain.


        :param item_category_label: The item_category_label of this Domain.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                item_category_label is not None and len(item_category_label) > 32):
            raise ValueError("Invalid value for `item_category_label`, length must be less than or equal to `32`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                item_category_label is not None and len(item_category_label) < 0):
            raise ValueError("Invalid value for `item_category_label`, length must be greater than or equal to `0`")  # noqa: E501

        self._item_category_label = item_category_label

    @property
    def item_list(self):
        """Gets the item_list of this Domain.  # noqa: E501


        :return: The item_list of this Domain.  # noqa: E501
        :rtype: list[Item]
        """
        return self._item_list

    @item_list.setter
    def item_list(self, item_list):
        """Sets the item_list of this Domain.


        :param item_list: The item_list of this Domain.  # noqa: E501
        :type: list[Item]
        """

        self._item_list = item_list

    @property
    def property_type_list(self):
        """Gets the property_type_list of this Domain.  # noqa: E501


        :return: The property_type_list of this Domain.  # noqa: E501
        :rtype: list[PropertyType]
        """
        return self._property_type_list

    @property_type_list.setter
    def property_type_list(self, property_type_list):
        """Sets the property_type_list of this Domain.


        :param property_type_list: The property_type_list of this Domain.  # noqa: E501
        :type: list[PropertyType]
        """

        self._property_type_list = property_type_list

    @property
    def item_type_list(self):
        """Gets the item_type_list of this Domain.  # noqa: E501


        :return: The item_type_list of this Domain.  # noqa: E501
        :rtype: list[ItemType]
        """
        return self._item_type_list

    @item_type_list.setter
    def item_type_list(self, item_type_list):
        """Sets the item_type_list of this Domain.


        :param item_type_list: The item_type_list of this Domain.  # noqa: E501
        :type: list[ItemType]
        """

        self._item_type_list = item_type_list

    @property
    def item_category_list(self):
        """Gets the item_category_list of this Domain.  # noqa: E501


        :return: The item_category_list of this Domain.  # noqa: E501
        :rtype: list[ItemCategory]
        """
        return self._item_category_list

    @item_category_list.setter
    def item_category_list(self, item_category_list):
        """Sets the item_category_list of this Domain.


        :param item_category_list: The item_category_list of this Domain.  # noqa: E501
        :type: list[ItemCategory]
        """

        self._item_category_list = item_category_list

    @property
    def allowed_entity_type_list(self):
        """Gets the allowed_entity_type_list of this Domain.  # noqa: E501


        :return: The allowed_entity_type_list of this Domain.  # noqa: E501
        :rtype: list[EntityType]
        """
        return self._allowed_entity_type_list

    @allowed_entity_type_list.setter
    def allowed_entity_type_list(self, allowed_entity_type_list):
        """Sets the allowed_entity_type_list of this Domain.


        :param allowed_entity_type_list: The allowed_entity_type_list of this Domain.  # noqa: E501
        :type: list[EntityType]
        """

        self._allowed_entity_type_list = allowed_entity_type_list

    @property
    def domain_rep_icon(self):
        """Gets the domain_rep_icon of this Domain.  # noqa: E501


        :return: The domain_rep_icon of this Domain.  # noqa: E501
        :rtype: str
        """
        return self._domain_rep_icon

    @domain_rep_icon.setter
    def domain_rep_icon(self, domain_rep_icon):
        """Sets the domain_rep_icon of this Domain.


        :param domain_rep_icon: The domain_rep_icon of this Domain.  # noqa: E501
        :type: str
        """

        self._domain_rep_icon = domain_rep_icon

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
        if not isinstance(other, Domain):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Domain):
            return True

        return self.to_dict() != other.to_dict()
