# generated from rosidl_generator_py/resource/_idl.py.em
# with input from interfaces:srv/GetLastPositions.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_GetLastPositions_Request(type):
    """Metaclass of message 'GetLastPositions_Request'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'interfaces.srv.GetLastPositions_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__get_last_positions__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__get_last_positions__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__get_last_positions__request
            cls._TYPE_SUPPORT = module.type_support_msg__srv__get_last_positions__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__get_last_positions__request

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class GetLastPositions_Request(metaclass=Metaclass_GetLastPositions_Request):
    """Message class 'GetLastPositions_Request'."""

    __slots__ = [
        '_num_positions',
    ]

    _fields_and_field_types = {
        'num_positions': 'int32',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.num_positions = kwargs.get('num_positions', int())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.num_positions != other.num_positions:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def num_positions(self):
        """Message field 'num_positions'."""
        return self._num_positions

    @num_positions.setter
    def num_positions(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'num_positions' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'num_positions' field must be an integer in [-2147483648, 2147483647]"
        self._num_positions = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_GetLastPositions_Response(type):
    """Metaclass of message 'GetLastPositions_Response'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'interfaces.srv.GetLastPositions_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__get_last_positions__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__get_last_positions__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__get_last_positions__response
            cls._TYPE_SUPPORT = module.type_support_msg__srv__get_last_positions__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__get_last_positions__response

            from interfaces.msg import Position
            if Position.__class__._TYPE_SUPPORT is None:
                Position.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class GetLastPositions_Response(metaclass=Metaclass_GetLastPositions_Response):
    """Message class 'GetLastPositions_Response'."""

    __slots__ = [
        '_positions',
    ]

    _fields_and_field_types = {
        'positions': 'sequence<interfaces/Position>',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.NamespacedType(['interfaces', 'msg'], 'Position')),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.positions = kwargs.get('positions', [])

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.positions != other.positions:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def positions(self):
        """Message field 'positions'."""
        return self._positions

    @positions.setter
    def positions(self, value):
        if __debug__:
            from interfaces.msg import Position
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, Position) for v in value) and
                 True), \
                "The 'positions' field must be a set or sequence and each value of type 'Position'"
        self._positions = value


class Metaclass_GetLastPositions(type):
    """Metaclass of service 'GetLastPositions'."""

    _TYPE_SUPPORT = None

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'interfaces.srv.GetLastPositions')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__srv__get_last_positions

            from interfaces.srv import _get_last_positions
            if _get_last_positions.Metaclass_GetLastPositions_Request._TYPE_SUPPORT is None:
                _get_last_positions.Metaclass_GetLastPositions_Request.__import_type_support__()
            if _get_last_positions.Metaclass_GetLastPositions_Response._TYPE_SUPPORT is None:
                _get_last_positions.Metaclass_GetLastPositions_Response.__import_type_support__()


class GetLastPositions(metaclass=Metaclass_GetLastPositions):
    from interfaces.srv._get_last_positions import GetLastPositions_Request as Request
    from interfaces.srv._get_last_positions import GetLastPositions_Response as Response

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')
