# coding: utf-8

"""
    Assetic Integration API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: v2
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

##from assetic.models.embedded_resource import EmbeddedResource  # noqa: F401,E501
##from assetic.models.link import Link  # noqa: F401,E501


class FailureSubCode(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'id': 'int',
        'sub_code_number': 'str',
        'sub_notation': 'str',
        'description': 'str',
        'priority_factor': 'str',
        'links': 'list[Link]',
        'embedded': 'list[EmbeddedResource]'
    }

    attribute_map = {
        'id': 'Id',
        'sub_code_number': 'SubCodeNumber',
        'sub_notation': 'SubNotation',
        'description': 'Description',
        'priority_factor': 'PriorityFactor',
        'links': '_links',
        'embedded': '_embedded'
    }

    def __init__(self, id=None, sub_code_number=None, sub_notation=None, description=None, priority_factor=None, links=None, embedded=None):  # noqa: E501
        """FailureSubCode - a model defined in Swagger"""  # noqa: E501

        self._id = None
        self._sub_code_number = None
        self._sub_notation = None
        self._description = None
        self._priority_factor = None
        self._links = None
        self._embedded = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if sub_code_number is not None:
            self.sub_code_number = sub_code_number
        if sub_notation is not None:
            self.sub_notation = sub_notation
        if description is not None:
            self.description = description
        if priority_factor is not None:
            self.priority_factor = priority_factor
        if links is not None:
            self.links = links
        if embedded is not None:
            self.embedded = embedded

    @property
    def id(self):
        """Gets the id of this FailureSubCode.  # noqa: E501


        :return: The id of this FailureSubCode.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this FailureSubCode.


        :param id: The id of this FailureSubCode.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def sub_code_number(self):
        """Gets the sub_code_number of this FailureSubCode.  # noqa: E501


        :return: The sub_code_number of this FailureSubCode.  # noqa: E501
        :rtype: str
        """
        return self._sub_code_number

    @sub_code_number.setter
    def sub_code_number(self, sub_code_number):
        """Sets the sub_code_number of this FailureSubCode.


        :param sub_code_number: The sub_code_number of this FailureSubCode.  # noqa: E501
        :type: str
        """

        self._sub_code_number = sub_code_number

    @property
    def sub_notation(self):
        """Gets the sub_notation of this FailureSubCode.  # noqa: E501


        :return: The sub_notation of this FailureSubCode.  # noqa: E501
        :rtype: str
        """
        return self._sub_notation

    @sub_notation.setter
    def sub_notation(self, sub_notation):
        """Sets the sub_notation of this FailureSubCode.


        :param sub_notation: The sub_notation of this FailureSubCode.  # noqa: E501
        :type: str
        """

        self._sub_notation = sub_notation

    @property
    def description(self):
        """Gets the description of this FailureSubCode.  # noqa: E501


        :return: The description of this FailureSubCode.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this FailureSubCode.


        :param description: The description of this FailureSubCode.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def priority_factor(self):
        """Gets the priority_factor of this FailureSubCode.  # noqa: E501


        :return: The priority_factor of this FailureSubCode.  # noqa: E501
        :rtype: str
        """
        return self._priority_factor

    @priority_factor.setter
    def priority_factor(self, priority_factor):
        """Sets the priority_factor of this FailureSubCode.


        :param priority_factor: The priority_factor of this FailureSubCode.  # noqa: E501
        :type: str
        """

        self._priority_factor = priority_factor

    @property
    def links(self):
        """Gets the links of this FailureSubCode.  # noqa: E501


        :return: The links of this FailureSubCode.  # noqa: E501
        :rtype: list[Link]
        """
        return self._links

    @links.setter
    def links(self, links):
        """Sets the links of this FailureSubCode.


        :param links: The links of this FailureSubCode.  # noqa: E501
        :type: list[Link]
        """

        self._links = links

    @property
    def embedded(self):
        """Gets the embedded of this FailureSubCode.  # noqa: E501


        :return: The embedded of this FailureSubCode.  # noqa: E501
        :rtype: list[EmbeddedResource]
        """
        return self._embedded

    @embedded.setter
    def embedded(self, embedded):
        """Sets the embedded of this FailureSubCode.


        :param embedded: The embedded of this FailureSubCode.  # noqa: E501
        :type: list[EmbeddedResource]
        """

        self._embedded = embedded

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
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
        if issubclass(FailureSubCode, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, FailureSubCode):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
