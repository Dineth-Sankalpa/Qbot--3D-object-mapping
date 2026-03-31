// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from interfaces:srv/GetLastPositions.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES__SRV__DETAIL__GET_LAST_POSITIONS__STRUCT_HPP_
#define INTERFACES__SRV__DETAIL__GET_LAST_POSITIONS__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__interfaces__srv__GetLastPositions_Request __attribute__((deprecated))
#else
# define DEPRECATED__interfaces__srv__GetLastPositions_Request __declspec(deprecated)
#endif

namespace interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct GetLastPositions_Request_
{
  using Type = GetLastPositions_Request_<ContainerAllocator>;

  explicit GetLastPositions_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->num_positions = 0l;
    }
  }

  explicit GetLastPositions_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->num_positions = 0l;
    }
  }

  // field types and members
  using _num_positions_type =
    int32_t;
  _num_positions_type num_positions;

  // setters for named parameter idiom
  Type & set__num_positions(
    const int32_t & _arg)
  {
    this->num_positions = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    interfaces::srv::GetLastPositions_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const interfaces::srv::GetLastPositions_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<interfaces::srv::GetLastPositions_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<interfaces::srv::GetLastPositions_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      interfaces::srv::GetLastPositions_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<interfaces::srv::GetLastPositions_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      interfaces::srv::GetLastPositions_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<interfaces::srv::GetLastPositions_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<interfaces::srv::GetLastPositions_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<interfaces::srv::GetLastPositions_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__interfaces__srv__GetLastPositions_Request
    std::shared_ptr<interfaces::srv::GetLastPositions_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__interfaces__srv__GetLastPositions_Request
    std::shared_ptr<interfaces::srv::GetLastPositions_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const GetLastPositions_Request_ & other) const
  {
    if (this->num_positions != other.num_positions) {
      return false;
    }
    return true;
  }
  bool operator!=(const GetLastPositions_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct GetLastPositions_Request_

// alias to use template instance with default allocator
using GetLastPositions_Request =
  interfaces::srv::GetLastPositions_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace interfaces


// Include directives for member types
// Member 'positions'
#include "interfaces/msg/detail/position__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__interfaces__srv__GetLastPositions_Response __attribute__((deprecated))
#else
# define DEPRECATED__interfaces__srv__GetLastPositions_Response __declspec(deprecated)
#endif

namespace interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct GetLastPositions_Response_
{
  using Type = GetLastPositions_Response_<ContainerAllocator>;

  explicit GetLastPositions_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
  }

  explicit GetLastPositions_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
    (void)_alloc;
  }

  // field types and members
  using _positions_type =
    std::vector<interfaces::msg::Position_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<interfaces::msg::Position_<ContainerAllocator>>>;
  _positions_type positions;

  // setters for named parameter idiom
  Type & set__positions(
    const std::vector<interfaces::msg::Position_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<interfaces::msg::Position_<ContainerAllocator>>> & _arg)
  {
    this->positions = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    interfaces::srv::GetLastPositions_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const interfaces::srv::GetLastPositions_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<interfaces::srv::GetLastPositions_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<interfaces::srv::GetLastPositions_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      interfaces::srv::GetLastPositions_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<interfaces::srv::GetLastPositions_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      interfaces::srv::GetLastPositions_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<interfaces::srv::GetLastPositions_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<interfaces::srv::GetLastPositions_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<interfaces::srv::GetLastPositions_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__interfaces__srv__GetLastPositions_Response
    std::shared_ptr<interfaces::srv::GetLastPositions_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__interfaces__srv__GetLastPositions_Response
    std::shared_ptr<interfaces::srv::GetLastPositions_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const GetLastPositions_Response_ & other) const
  {
    if (this->positions != other.positions) {
      return false;
    }
    return true;
  }
  bool operator!=(const GetLastPositions_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct GetLastPositions_Response_

// alias to use template instance with default allocator
using GetLastPositions_Response =
  interfaces::srv::GetLastPositions_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace interfaces

namespace interfaces
{

namespace srv
{

struct GetLastPositions
{
  using Request = interfaces::srv::GetLastPositions_Request;
  using Response = interfaces::srv::GetLastPositions_Response;
};

}  // namespace srv

}  // namespace interfaces

#endif  // INTERFACES__SRV__DETAIL__GET_LAST_POSITIONS__STRUCT_HPP_
