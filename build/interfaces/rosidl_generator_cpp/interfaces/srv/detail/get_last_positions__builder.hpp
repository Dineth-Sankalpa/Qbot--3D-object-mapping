// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from interfaces:srv/GetLastPositions.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES__SRV__DETAIL__GET_LAST_POSITIONS__BUILDER_HPP_
#define INTERFACES__SRV__DETAIL__GET_LAST_POSITIONS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "interfaces/srv/detail/get_last_positions__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace interfaces
{

namespace srv
{

namespace builder
{

class Init_GetLastPositions_Request_num_positions
{
public:
  Init_GetLastPositions_Request_num_positions()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::interfaces::srv::GetLastPositions_Request num_positions(::interfaces::srv::GetLastPositions_Request::_num_positions_type arg)
  {
    msg_.num_positions = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interfaces::srv::GetLastPositions_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::interfaces::srv::GetLastPositions_Request>()
{
  return interfaces::srv::builder::Init_GetLastPositions_Request_num_positions();
}

}  // namespace interfaces


namespace interfaces
{

namespace srv
{

namespace builder
{

class Init_GetLastPositions_Response_positions
{
public:
  Init_GetLastPositions_Response_positions()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::interfaces::srv::GetLastPositions_Response positions(::interfaces::srv::GetLastPositions_Response::_positions_type arg)
  {
    msg_.positions = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interfaces::srv::GetLastPositions_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::interfaces::srv::GetLastPositions_Response>()
{
  return interfaces::srv::builder::Init_GetLastPositions_Response_positions();
}

}  // namespace interfaces

#endif  // INTERFACES__SRV__DETAIL__GET_LAST_POSITIONS__BUILDER_HPP_
