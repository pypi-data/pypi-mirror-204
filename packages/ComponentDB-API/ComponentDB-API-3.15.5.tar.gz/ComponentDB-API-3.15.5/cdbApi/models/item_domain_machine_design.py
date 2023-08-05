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


class ItemDomainMachineDesign(object):
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
        'item_identifier1': 'str',
        'item_identifier2': 'str',
        'qr_id': 'int',
        'domain': 'Domain',
        'derived_from_item': 'Item',
        'domain_id': 'int',
        'item_category_list_import': 'list[ItemCategory]',
        'primary_image_for_item': 'str',
        'item_control': 'bool',
        'max_sort_order': 'float',
        'description': 'str',
        'entity_type_list': 'list[EntityType]',
        'item_category_list': 'list[ItemCategory]',
        'item_type_list': 'list[ItemType]',
        'item_project_list': 'list[ItemProject]',
        'item_source_list': 'list[ItemSource]',
        'membership_loaded': 'bool',
        'move_to_trash_error_msg': 'str',
        'move_to_trash_warning_msg': 'str',
        'assigned_item': 'Item',
        'is_housed': 'bool',
        'alternate_name': 'str',
        'assigned_represented_element': 'ItemElement',
        'status_property_type_name': 'str',
        'move_to_trash_row_style': 'str',
        'location_item': 'ItemDomainLocation'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'item_identifier1': 'itemIdentifier1',
        'item_identifier2': 'itemIdentifier2',
        'qr_id': 'qrId',
        'domain': 'domain',
        'derived_from_item': 'derivedFromItem',
        'domain_id': 'domainId',
        'item_category_list_import': 'itemCategoryListImport',
        'primary_image_for_item': 'primaryImageForItem',
        'item_control': 'itemControl',
        'max_sort_order': 'maxSortOrder',
        'description': 'description',
        'entity_type_list': 'entityTypeList',
        'item_category_list': 'itemCategoryList',
        'item_type_list': 'itemTypeList',
        'item_project_list': 'itemProjectList',
        'item_source_list': 'itemSourceList',
        'membership_loaded': 'membershipLoaded',
        'move_to_trash_error_msg': 'moveToTrashErrorMsg',
        'move_to_trash_warning_msg': 'moveToTrashWarningMsg',
        'assigned_item': 'assignedItem',
        'is_housed': 'isHoused',
        'alternate_name': 'alternateName',
        'assigned_represented_element': 'assignedRepresentedElement',
        'status_property_type_name': 'statusPropertyTypeName',
        'move_to_trash_row_style': 'moveToTrashRowStyle',
        'location_item': 'locationItem'
    }

    def __init__(self, id=None, name=None, item_identifier1=None, item_identifier2=None, qr_id=None, domain=None, derived_from_item=None, domain_id=None, item_category_list_import=None, primary_image_for_item=None, item_control=None, max_sort_order=None, description=None, entity_type_list=None, item_category_list=None, item_type_list=None, item_project_list=None, item_source_list=None, membership_loaded=None, move_to_trash_error_msg=None, move_to_trash_warning_msg=None, assigned_item=None, is_housed=None, alternate_name=None, assigned_represented_element=None, status_property_type_name=None, move_to_trash_row_style=None, location_item=None, local_vars_configuration=None):  # noqa: E501
        """ItemDomainMachineDesign - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._name = None
        self._item_identifier1 = None
        self._item_identifier2 = None
        self._qr_id = None
        self._domain = None
        self._derived_from_item = None
        self._domain_id = None
        self._item_category_list_import = None
        self._primary_image_for_item = None
        self._item_control = None
        self._max_sort_order = None
        self._description = None
        self._entity_type_list = None
        self._item_category_list = None
        self._item_type_list = None
        self._item_project_list = None
        self._item_source_list = None
        self._membership_loaded = None
        self._move_to_trash_error_msg = None
        self._move_to_trash_warning_msg = None
        self._assigned_item = None
        self._is_housed = None
        self._alternate_name = None
        self._assigned_represented_element = None
        self._status_property_type_name = None
        self._move_to_trash_row_style = None
        self._location_item = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if item_identifier1 is not None:
            self.item_identifier1 = item_identifier1
        if item_identifier2 is not None:
            self.item_identifier2 = item_identifier2
        if qr_id is not None:
            self.qr_id = qr_id
        if domain is not None:
            self.domain = domain
        if derived_from_item is not None:
            self.derived_from_item = derived_from_item
        if domain_id is not None:
            self.domain_id = domain_id
        if item_category_list_import is not None:
            self.item_category_list_import = item_category_list_import
        if primary_image_for_item is not None:
            self.primary_image_for_item = primary_image_for_item
        if item_control is not None:
            self.item_control = item_control
        if max_sort_order is not None:
            self.max_sort_order = max_sort_order
        if description is not None:
            self.description = description
        if entity_type_list is not None:
            self.entity_type_list = entity_type_list
        if item_category_list is not None:
            self.item_category_list = item_category_list
        if item_type_list is not None:
            self.item_type_list = item_type_list
        if item_project_list is not None:
            self.item_project_list = item_project_list
        if item_source_list is not None:
            self.item_source_list = item_source_list
        if membership_loaded is not None:
            self.membership_loaded = membership_loaded
        if move_to_trash_error_msg is not None:
            self.move_to_trash_error_msg = move_to_trash_error_msg
        if move_to_trash_warning_msg is not None:
            self.move_to_trash_warning_msg = move_to_trash_warning_msg
        if assigned_item is not None:
            self.assigned_item = assigned_item
        if is_housed is not None:
            self.is_housed = is_housed
        if alternate_name is not None:
            self.alternate_name = alternate_name
        if assigned_represented_element is not None:
            self.assigned_represented_element = assigned_represented_element
        if status_property_type_name is not None:
            self.status_property_type_name = status_property_type_name
        if move_to_trash_row_style is not None:
            self.move_to_trash_row_style = move_to_trash_row_style
        if location_item is not None:
            self.location_item = location_item

    @property
    def id(self):
        """Gets the id of this ItemDomainMachineDesign.  # noqa: E501


        :return: The id of this ItemDomainMachineDesign.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ItemDomainMachineDesign.


        :param id: The id of this ItemDomainMachineDesign.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this ItemDomainMachineDesign.  # noqa: E501


        :return: The name of this ItemDomainMachineDesign.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ItemDomainMachineDesign.


        :param name: The name of this ItemDomainMachineDesign.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                name is not None and len(name) > 128):
            raise ValueError("Invalid value for `name`, length must be less than or equal to `128`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                name is not None and len(name) < 0):
            raise ValueError("Invalid value for `name`, length must be greater than or equal to `0`")  # noqa: E501

        self._name = name

    @property
    def item_identifier1(self):
        """Gets the item_identifier1 of this ItemDomainMachineDesign.  # noqa: E501


        :return: The item_identifier1 of this ItemDomainMachineDesign.  # noqa: E501
        :rtype: str
        """
        return self._item_identifier1

    @item_identifier1.setter
    def item_identifier1(self, item_identifier1):
        """Sets the item_identifier1 of this ItemDomainMachineDesign.


        :param item_identifier1: The item_identifier1 of this ItemDomainMachineDesign.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                item_identifier1 is not None and len(item_identifier1) > 128):
            raise ValueError("Invalid value for `item_identifier1`, length must be less than or equal to `128`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                item_identifier1 is not None and len(item_identifier1) < 0):
            raise ValueError("Invalid value for `item_identifier1`, length must be greater than or equal to `0`")  # noqa: E501

        self._item_identifier1 = item_identifier1

    @property
    def item_identifier2(self):
        """Gets the item_identifier2 of this ItemDomainMachineDesign.  # noqa: E501


        :return: The item_identifier2 of this ItemDomainMachineDesign.  # noqa: E501
        :rtype: str
        """
        return self._item_identifier2

    @item_identifier2.setter
    def item_identifier2(self, item_identifier2):
        """Sets the item_identifier2 of this ItemDomainMachineDesign.


        :param item_identifier2: The item_identifier2 of this ItemDomainMachineDesign.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                item_identifier2 is not None and len(item_identifier2) > 128):
            raise ValueError("Invalid value for `item_identifier2`, length must be less than or equal to `128`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                item_identifier2 is not None and len(item_identifier2) < 0):
            raise ValueError("Invalid value for `item_identifier2`, length must be greater than or equal to `0`")  # noqa: E501

        self._item_identifier2 = item_identifier2

    @property
    def qr_id(self):
        """Gets the qr_id of this ItemDomainMachineDesign.  # noqa: E501


        :return: The qr_id of this ItemDomainMachineDesign.  # noqa: E501
        :rtype: int
        """
        return self._qr_id

    @qr_id.setter
    def qr_id(self, qr_id):
        """Sets the qr_id of this ItemDomainMachineDesign.


        :param qr_id: The qr_id of this ItemDomainMachineDesign.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                qr_id is not None and qr_id < 0):  # noqa: E501
            raise ValueError("Invalid value for `qr_id`, must be a value greater than or equal to `0`")  # noqa: E501

        self._qr_id = qr_id

    @property
    def domain(self):
        """Gets the domain of this ItemDomainMachineDesign.  # noqa: E501


        :return: The domain of this ItemDomainMachineDesign.  # noqa: E501
        :rtype: Domain
        """
        return self._domain

    @domain.setter
    def domain(self, domain):
        """Sets the domain of this ItemDomainMachineDesign.


        :param domain: The domain of this ItemDomainMachineDesign.  # noqa: E501
        :type: Domain
        """

        self._domain = domain

    @property
    def derived_from_item(self):
        """Gets the derived_from_item of this ItemDomainMachineDesign.  # noqa: E501


        :return: The derived_from_item of this ItemDomainMachineDesign.  # noqa: E501
        :rtype: Item
        """
        return self._derived_from_item

    @derived_from_item.setter
    def derived_from_item(self, derived_from_item):
        """Sets the derived_from_item of this ItemDomainMachineDesign.


        :param derived_from_item: The derived_from_item of this ItemDomainMachineDesign.  # noqa: E501
        :type: Item
        """

        self._derived_from_item = derived_from_item

    @property
    def domain_id(self):
        """Gets the domain_id of this ItemDomainMachineDesign.  # noqa: E501


        :return: The domain_id of this ItemDomainMachineDesign.  # noqa: E501
        :rtype: int
        """
        return self._domain_id

    @domain_id.setter
    def domain_id(self, domain_id):
        """Sets the domain_id of this ItemDomainMachineDesign.


        :param domain_id: The domain_id of this ItemDomainMachineDesign.  # noqa: E501
        :type: int
        """

        self._domain_id = domain_id

    @property
    def item_category_list_import(self):
        """Gets the item_category_list_import of this ItemDomainMachineDesign.  # noqa: E501


        :return: The item_category_list_import of this ItemDomainMachineDesign.  # noqa: E501
        :rtype: list[ItemCategory]
        """
        return self._item_category_list_import

    @item_category_list_import.setter
    def item_category_list_import(self, item_category_list_import):
        """Sets the item_category_list_import of this ItemDomainMachineDesign.


        :param item_category_list_import: The item_category_list_import of this ItemDomainMachineDesign.  # noqa: E501
        :type: list[ItemCategory]
        """

        self._item_category_list_import = item_category_list_import

    @property
    def primary_image_for_item(self):
        """Gets the primary_image_for_item of this ItemDomainMachineDesign.  # noqa: E501


        :return: The primary_image_for_item of this ItemDomainMachineDesign.  # noqa: E501
        :rtype: str
        """
        return self._primary_image_for_item

    @primary_image_for_item.setter
    def primary_image_for_item(self, primary_image_for_item):
        """Sets the primary_image_for_item of this ItemDomainMachineDesign.


        :param primary_image_for_item: The primary_image_for_item of this ItemDomainMachineDesign.  # noqa: E501
        :type: str
        """

        self._primary_image_for_item = primary_image_for_item

    @property
    def item_control(self):
        """Gets the item_control of this ItemDomainMachineDesign.  # noqa: E501


        :return: The item_control of this ItemDomainMachineDesign.  # noqa: E501
        :rtype: bool
        """
        return self._item_control

    @item_control.setter
    def item_control(self, item_control):
        """Sets the item_control of this ItemDomainMachineDesign.


        :param item_control: The item_control of this ItemDomainMachineDesign.  # noqa: E501
        :type: bool
        """

        self._item_control = item_control

    @property
    def max_sort_order(self):
        """Gets the max_sort_order of this ItemDomainMachineDesign.  # noqa: E501


        :return: The max_sort_order of this ItemDomainMachineDesign.  # noqa: E501
        :rtype: float
        """
        return self._max_sort_order

    @max_sort_order.setter
    def max_sort_order(self, max_sort_order):
        """Sets the max_sort_order of this ItemDomainMachineDesign.


        :param max_sort_order: The max_sort_order of this ItemDomainMachineDesign.  # noqa: E501
        :type: float
        """

        self._max_sort_order = max_sort_order

    @property
    def description(self):
        """Gets the description of this ItemDomainMachineDesign.  # noqa: E501


        :return: The description of this ItemDomainMachineDesign.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this ItemDomainMachineDesign.


        :param description: The description of this ItemDomainMachineDesign.  # noqa: E501
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
    def entity_type_list(self):
        """Gets the entity_type_list of this ItemDomainMachineDesign.  # noqa: E501


        :return: The entity_type_list of this ItemDomainMachineDesign.  # noqa: E501
        :rtype: list[EntityType]
        """
        return self._entity_type_list

    @entity_type_list.setter
    def entity_type_list(self, entity_type_list):
        """Sets the entity_type_list of this ItemDomainMachineDesign.


        :param entity_type_list: The entity_type_list of this ItemDomainMachineDesign.  # noqa: E501
        :type: list[EntityType]
        """

        self._entity_type_list = entity_type_list

    @property
    def item_category_list(self):
        """Gets the item_category_list of this ItemDomainMachineDesign.  # noqa: E501


        :return: The item_category_list of this ItemDomainMachineDesign.  # noqa: E501
        :rtype: list[ItemCategory]
        """
        return self._item_category_list

    @item_category_list.setter
    def item_category_list(self, item_category_list):
        """Sets the item_category_list of this ItemDomainMachineDesign.


        :param item_category_list: The item_category_list of this ItemDomainMachineDesign.  # noqa: E501
        :type: list[ItemCategory]
        """

        self._item_category_list = item_category_list

    @property
    def item_type_list(self):
        """Gets the item_type_list of this ItemDomainMachineDesign.  # noqa: E501


        :return: The item_type_list of this ItemDomainMachineDesign.  # noqa: E501
        :rtype: list[ItemType]
        """
        return self._item_type_list

    @item_type_list.setter
    def item_type_list(self, item_type_list):
        """Sets the item_type_list of this ItemDomainMachineDesign.


        :param item_type_list: The item_type_list of this ItemDomainMachineDesign.  # noqa: E501
        :type: list[ItemType]
        """

        self._item_type_list = item_type_list

    @property
    def item_project_list(self):
        """Gets the item_project_list of this ItemDomainMachineDesign.  # noqa: E501


        :return: The item_project_list of this ItemDomainMachineDesign.  # noqa: E501
        :rtype: list[ItemProject]
        """
        return self._item_project_list

    @item_project_list.setter
    def item_project_list(self, item_project_list):
        """Sets the item_project_list of this ItemDomainMachineDesign.


        :param item_project_list: The item_project_list of this ItemDomainMachineDesign.  # noqa: E501
        :type: list[ItemProject]
        """

        self._item_project_list = item_project_list

    @property
    def item_source_list(self):
        """Gets the item_source_list of this ItemDomainMachineDesign.  # noqa: E501


        :return: The item_source_list of this ItemDomainMachineDesign.  # noqa: E501
        :rtype: list[ItemSource]
        """
        return self._item_source_list

    @item_source_list.setter
    def item_source_list(self, item_source_list):
        """Sets the item_source_list of this ItemDomainMachineDesign.


        :param item_source_list: The item_source_list of this ItemDomainMachineDesign.  # noqa: E501
        :type: list[ItemSource]
        """

        self._item_source_list = item_source_list

    @property
    def membership_loaded(self):
        """Gets the membership_loaded of this ItemDomainMachineDesign.  # noqa: E501


        :return: The membership_loaded of this ItemDomainMachineDesign.  # noqa: E501
        :rtype: bool
        """
        return self._membership_loaded

    @membership_loaded.setter
    def membership_loaded(self, membership_loaded):
        """Sets the membership_loaded of this ItemDomainMachineDesign.


        :param membership_loaded: The membership_loaded of this ItemDomainMachineDesign.  # noqa: E501
        :type: bool
        """

        self._membership_loaded = membership_loaded

    @property
    def move_to_trash_error_msg(self):
        """Gets the move_to_trash_error_msg of this ItemDomainMachineDesign.  # noqa: E501


        :return: The move_to_trash_error_msg of this ItemDomainMachineDesign.  # noqa: E501
        :rtype: str
        """
        return self._move_to_trash_error_msg

    @move_to_trash_error_msg.setter
    def move_to_trash_error_msg(self, move_to_trash_error_msg):
        """Sets the move_to_trash_error_msg of this ItemDomainMachineDesign.


        :param move_to_trash_error_msg: The move_to_trash_error_msg of this ItemDomainMachineDesign.  # noqa: E501
        :type: str
        """

        self._move_to_trash_error_msg = move_to_trash_error_msg

    @property
    def move_to_trash_warning_msg(self):
        """Gets the move_to_trash_warning_msg of this ItemDomainMachineDesign.  # noqa: E501


        :return: The move_to_trash_warning_msg of this ItemDomainMachineDesign.  # noqa: E501
        :rtype: str
        """
        return self._move_to_trash_warning_msg

    @move_to_trash_warning_msg.setter
    def move_to_trash_warning_msg(self, move_to_trash_warning_msg):
        """Sets the move_to_trash_warning_msg of this ItemDomainMachineDesign.


        :param move_to_trash_warning_msg: The move_to_trash_warning_msg of this ItemDomainMachineDesign.  # noqa: E501
        :type: str
        """

        self._move_to_trash_warning_msg = move_to_trash_warning_msg

    @property
    def assigned_item(self):
        """Gets the assigned_item of this ItemDomainMachineDesign.  # noqa: E501


        :return: The assigned_item of this ItemDomainMachineDesign.  # noqa: E501
        :rtype: Item
        """
        return self._assigned_item

    @assigned_item.setter
    def assigned_item(self, assigned_item):
        """Sets the assigned_item of this ItemDomainMachineDesign.


        :param assigned_item: The assigned_item of this ItemDomainMachineDesign.  # noqa: E501
        :type: Item
        """

        self._assigned_item = assigned_item

    @property
    def is_housed(self):
        """Gets the is_housed of this ItemDomainMachineDesign.  # noqa: E501


        :return: The is_housed of this ItemDomainMachineDesign.  # noqa: E501
        :rtype: bool
        """
        return self._is_housed

    @is_housed.setter
    def is_housed(self, is_housed):
        """Sets the is_housed of this ItemDomainMachineDesign.


        :param is_housed: The is_housed of this ItemDomainMachineDesign.  # noqa: E501
        :type: bool
        """

        self._is_housed = is_housed

    @property
    def alternate_name(self):
        """Gets the alternate_name of this ItemDomainMachineDesign.  # noqa: E501


        :return: The alternate_name of this ItemDomainMachineDesign.  # noqa: E501
        :rtype: str
        """
        return self._alternate_name

    @alternate_name.setter
    def alternate_name(self, alternate_name):
        """Sets the alternate_name of this ItemDomainMachineDesign.


        :param alternate_name: The alternate_name of this ItemDomainMachineDesign.  # noqa: E501
        :type: str
        """

        self._alternate_name = alternate_name

    @property
    def assigned_represented_element(self):
        """Gets the assigned_represented_element of this ItemDomainMachineDesign.  # noqa: E501


        :return: The assigned_represented_element of this ItemDomainMachineDesign.  # noqa: E501
        :rtype: ItemElement
        """
        return self._assigned_represented_element

    @assigned_represented_element.setter
    def assigned_represented_element(self, assigned_represented_element):
        """Sets the assigned_represented_element of this ItemDomainMachineDesign.


        :param assigned_represented_element: The assigned_represented_element of this ItemDomainMachineDesign.  # noqa: E501
        :type: ItemElement
        """

        self._assigned_represented_element = assigned_represented_element

    @property
    def status_property_type_name(self):
        """Gets the status_property_type_name of this ItemDomainMachineDesign.  # noqa: E501


        :return: The status_property_type_name of this ItemDomainMachineDesign.  # noqa: E501
        :rtype: str
        """
        return self._status_property_type_name

    @status_property_type_name.setter
    def status_property_type_name(self, status_property_type_name):
        """Sets the status_property_type_name of this ItemDomainMachineDesign.


        :param status_property_type_name: The status_property_type_name of this ItemDomainMachineDesign.  # noqa: E501
        :type: str
        """

        self._status_property_type_name = status_property_type_name

    @property
    def move_to_trash_row_style(self):
        """Gets the move_to_trash_row_style of this ItemDomainMachineDesign.  # noqa: E501


        :return: The move_to_trash_row_style of this ItemDomainMachineDesign.  # noqa: E501
        :rtype: str
        """
        return self._move_to_trash_row_style

    @move_to_trash_row_style.setter
    def move_to_trash_row_style(self, move_to_trash_row_style):
        """Sets the move_to_trash_row_style of this ItemDomainMachineDesign.


        :param move_to_trash_row_style: The move_to_trash_row_style of this ItemDomainMachineDesign.  # noqa: E501
        :type: str
        """

        self._move_to_trash_row_style = move_to_trash_row_style

    @property
    def location_item(self):
        """Gets the location_item of this ItemDomainMachineDesign.  # noqa: E501


        :return: The location_item of this ItemDomainMachineDesign.  # noqa: E501
        :rtype: ItemDomainLocation
        """
        return self._location_item

    @location_item.setter
    def location_item(self, location_item):
        """Sets the location_item of this ItemDomainMachineDesign.


        :param location_item: The location_item of this ItemDomainMachineDesign.  # noqa: E501
        :type: ItemDomainLocation
        """

        self._location_item = location_item

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
        if not isinstance(other, ItemDomainMachineDesign):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ItemDomainMachineDesign):
            return True

        return self.to_dict() != other.to_dict()
