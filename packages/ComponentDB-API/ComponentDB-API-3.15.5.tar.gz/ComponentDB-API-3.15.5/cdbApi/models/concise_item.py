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


class ConciseItem(object):
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
        'id': 'int',
        'item_identifier1': 'str',
        'item_identifier2': 'str',
        'qr_id': 'int',
        'derived_from_item_id': 'int',
        'derived_from_item_name': 'str',
        'item_project_id_list': 'list[int]',
        'item_type_id_list': 'list[int]',
        'item_category_id_list': 'list[int]',
        'primary_image_for_item': 'str'
    }

    attribute_map = {
        'name': 'name',
        'id': 'id',
        'item_identifier1': 'itemIdentifier1',
        'item_identifier2': 'itemIdentifier2',
        'qr_id': 'qrId',
        'derived_from_item_id': 'derivedFromItemId',
        'derived_from_item_name': 'derivedFromItemName',
        'item_project_id_list': 'itemProjectIdList',
        'item_type_id_list': 'itemTypeIdList',
        'item_category_id_list': 'itemCategoryIdList',
        'primary_image_for_item': 'primaryImageForItem'
    }

    def __init__(self, name=None, id=None, item_identifier1=None, item_identifier2=None, qr_id=None, derived_from_item_id=None, derived_from_item_name=None, item_project_id_list=None, item_type_id_list=None, item_category_id_list=None, primary_image_for_item=None, local_vars_configuration=None):  # noqa: E501
        """ConciseItem - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._id = None
        self._item_identifier1 = None
        self._item_identifier2 = None
        self._qr_id = None
        self._derived_from_item_id = None
        self._derived_from_item_name = None
        self._item_project_id_list = None
        self._item_type_id_list = None
        self._item_category_id_list = None
        self._primary_image_for_item = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if id is not None:
            self.id = id
        if item_identifier1 is not None:
            self.item_identifier1 = item_identifier1
        if item_identifier2 is not None:
            self.item_identifier2 = item_identifier2
        if qr_id is not None:
            self.qr_id = qr_id
        if derived_from_item_id is not None:
            self.derived_from_item_id = derived_from_item_id
        if derived_from_item_name is not None:
            self.derived_from_item_name = derived_from_item_name
        if item_project_id_list is not None:
            self.item_project_id_list = item_project_id_list
        if item_type_id_list is not None:
            self.item_type_id_list = item_type_id_list
        if item_category_id_list is not None:
            self.item_category_id_list = item_category_id_list
        if primary_image_for_item is not None:
            self.primary_image_for_item = primary_image_for_item

    @property
    def name(self):
        """Gets the name of this ConciseItem.  # noqa: E501


        :return: The name of this ConciseItem.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ConciseItem.


        :param name: The name of this ConciseItem.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def id(self):
        """Gets the id of this ConciseItem.  # noqa: E501


        :return: The id of this ConciseItem.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ConciseItem.


        :param id: The id of this ConciseItem.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def item_identifier1(self):
        """Gets the item_identifier1 of this ConciseItem.  # noqa: E501


        :return: The item_identifier1 of this ConciseItem.  # noqa: E501
        :rtype: str
        """
        return self._item_identifier1

    @item_identifier1.setter
    def item_identifier1(self, item_identifier1):
        """Sets the item_identifier1 of this ConciseItem.


        :param item_identifier1: The item_identifier1 of this ConciseItem.  # noqa: E501
        :type: str
        """

        self._item_identifier1 = item_identifier1

    @property
    def item_identifier2(self):
        """Gets the item_identifier2 of this ConciseItem.  # noqa: E501


        :return: The item_identifier2 of this ConciseItem.  # noqa: E501
        :rtype: str
        """
        return self._item_identifier2

    @item_identifier2.setter
    def item_identifier2(self, item_identifier2):
        """Sets the item_identifier2 of this ConciseItem.


        :param item_identifier2: The item_identifier2 of this ConciseItem.  # noqa: E501
        :type: str
        """

        self._item_identifier2 = item_identifier2

    @property
    def qr_id(self):
        """Gets the qr_id of this ConciseItem.  # noqa: E501


        :return: The qr_id of this ConciseItem.  # noqa: E501
        :rtype: int
        """
        return self._qr_id

    @qr_id.setter
    def qr_id(self, qr_id):
        """Sets the qr_id of this ConciseItem.


        :param qr_id: The qr_id of this ConciseItem.  # noqa: E501
        :type: int
        """

        self._qr_id = qr_id

    @property
    def derived_from_item_id(self):
        """Gets the derived_from_item_id of this ConciseItem.  # noqa: E501


        :return: The derived_from_item_id of this ConciseItem.  # noqa: E501
        :rtype: int
        """
        return self._derived_from_item_id

    @derived_from_item_id.setter
    def derived_from_item_id(self, derived_from_item_id):
        """Sets the derived_from_item_id of this ConciseItem.


        :param derived_from_item_id: The derived_from_item_id of this ConciseItem.  # noqa: E501
        :type: int
        """

        self._derived_from_item_id = derived_from_item_id

    @property
    def derived_from_item_name(self):
        """Gets the derived_from_item_name of this ConciseItem.  # noqa: E501


        :return: The derived_from_item_name of this ConciseItem.  # noqa: E501
        :rtype: str
        """
        return self._derived_from_item_name

    @derived_from_item_name.setter
    def derived_from_item_name(self, derived_from_item_name):
        """Sets the derived_from_item_name of this ConciseItem.


        :param derived_from_item_name: The derived_from_item_name of this ConciseItem.  # noqa: E501
        :type: str
        """

        self._derived_from_item_name = derived_from_item_name

    @property
    def item_project_id_list(self):
        """Gets the item_project_id_list of this ConciseItem.  # noqa: E501


        :return: The item_project_id_list of this ConciseItem.  # noqa: E501
        :rtype: list[int]
        """
        return self._item_project_id_list

    @item_project_id_list.setter
    def item_project_id_list(self, item_project_id_list):
        """Sets the item_project_id_list of this ConciseItem.


        :param item_project_id_list: The item_project_id_list of this ConciseItem.  # noqa: E501
        :type: list[int]
        """

        self._item_project_id_list = item_project_id_list

    @property
    def item_type_id_list(self):
        """Gets the item_type_id_list of this ConciseItem.  # noqa: E501


        :return: The item_type_id_list of this ConciseItem.  # noqa: E501
        :rtype: list[int]
        """
        return self._item_type_id_list

    @item_type_id_list.setter
    def item_type_id_list(self, item_type_id_list):
        """Sets the item_type_id_list of this ConciseItem.


        :param item_type_id_list: The item_type_id_list of this ConciseItem.  # noqa: E501
        :type: list[int]
        """

        self._item_type_id_list = item_type_id_list

    @property
    def item_category_id_list(self):
        """Gets the item_category_id_list of this ConciseItem.  # noqa: E501


        :return: The item_category_id_list of this ConciseItem.  # noqa: E501
        :rtype: list[int]
        """
        return self._item_category_id_list

    @item_category_id_list.setter
    def item_category_id_list(self, item_category_id_list):
        """Sets the item_category_id_list of this ConciseItem.


        :param item_category_id_list: The item_category_id_list of this ConciseItem.  # noqa: E501
        :type: list[int]
        """

        self._item_category_id_list = item_category_id_list

    @property
    def primary_image_for_item(self):
        """Gets the primary_image_for_item of this ConciseItem.  # noqa: E501


        :return: The primary_image_for_item of this ConciseItem.  # noqa: E501
        :rtype: str
        """
        return self._primary_image_for_item

    @primary_image_for_item.setter
    def primary_image_for_item(self, primary_image_for_item):
        """Sets the primary_image_for_item of this ConciseItem.


        :param primary_image_for_item: The primary_image_for_item of this ConciseItem.  # noqa: E501
        :type: str
        """

        self._primary_image_for_item = primary_image_for_item

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
        if not isinstance(other, ConciseItem):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ConciseItem):
            return True

        return self.to_dict() != other.to_dict()
