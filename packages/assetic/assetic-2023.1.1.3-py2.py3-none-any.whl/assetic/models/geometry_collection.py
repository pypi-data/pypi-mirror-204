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

##from assetic.models.i_geometry_object import IGeometryObject  # noqa: F401,E501
##from assetic.models.icrs_object import ICRSObject  # noqa: F401,E501


class GeometryCollection(object):
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
        'type': 'str',
        'geometries': 'list[IGeometryObject]',
        'bbox': 'list[float]',
        'crs': 'ICRSObject'
    }

    attribute_map = {
        'type': 'type',
        'geometries': 'geometries',
        'bbox': 'bbox',
        'crs': 'crs'
    }

    def __init__(self, type=None, geometries=None, bbox=None, crs=None):  # noqa: E501
        """GeometryCollection - a model defined in Swagger"""  # noqa: E501

        self._type = None
        self._geometries = None
        self._bbox = None
        self._crs = None
        self.discriminator = None

        self.type = type
        self.geometries = geometries
        if bbox is not None:
            self.bbox = bbox
        if crs is not None:
            self.crs = crs

    @property
    def type(self):
        """Gets the type of this GeometryCollection.  # noqa: E501


        :return: The type of this GeometryCollection.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this GeometryCollection.


        :param type: The type of this GeometryCollection.  # noqa: E501
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501
        allowed_values = ["Point", "MultiPoint", "LineString", "MultiLineString", "Polygon", "MultiPolygon", "GeometryCollection", "Feature", "FeatureCollection"]  # noqa: E501
        if "None" in allowed_values:
            allowed_values.append(None)
        if type not in allowed_values:
            # Could be an integer enum returned by API
            try:
                int_type = int(type)
            except ValueError:
                raise ValueError(
                    "Invalid value for `type` ({0}), must be one of {1}"  # noqa: E501
                    .format(type, allowed_values)
                )

        self._type = type

    @property
    def geometries(self):
        """Gets the geometries of this GeometryCollection.  # noqa: E501


        :return: The geometries of this GeometryCollection.  # noqa: E501
        :rtype: list[IGeometryObject]
        """
        return self._geometries

    @geometries.setter
    def geometries(self, geometries):
        """Sets the geometries of this GeometryCollection.


        :param geometries: The geometries of this GeometryCollection.  # noqa: E501
        :type: list[IGeometryObject]
        """
        if geometries is None:
            raise ValueError("Invalid value for `geometries`, must not be `None`")  # noqa: E501

        self._geometries = geometries

    @property
    def bbox(self):
        """Gets the bbox of this GeometryCollection.  # noqa: E501


        :return: The bbox of this GeometryCollection.  # noqa: E501
        :rtype: list[float]
        """
        return self._bbox

    @bbox.setter
    def bbox(self, bbox):
        """Sets the bbox of this GeometryCollection.


        :param bbox: The bbox of this GeometryCollection.  # noqa: E501
        :type: list[float]
        """

        self._bbox = bbox

    @property
    def crs(self):
        """Gets the crs of this GeometryCollection.  # noqa: E501


        :return: The crs of this GeometryCollection.  # noqa: E501
        :rtype: ICRSObject
        """
        return self._crs

    @crs.setter
    def crs(self, crs):
        """Sets the crs of this GeometryCollection.


        :param crs: The crs of this GeometryCollection.  # noqa: E501
        :type: ICRSObject
        """

        self._crs = crs

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
        if issubclass(GeometryCollection, dict):
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
        if not isinstance(other, GeometryCollection):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
