// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from swarm_msgs:msg/DroneState.idl
// generated code does not contain a copyright notice

#ifndef SWARM_MSGS__MSG__DETAIL__DRONE_STATE__BUILDER_HPP_
#define SWARM_MSGS__MSG__DETAIL__DRONE_STATE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "swarm_msgs/msg/detail/drone_state__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace swarm_msgs
{

namespace msg
{

namespace builder
{

class Init_DroneState_timestamp
{
public:
  explicit Init_DroneState_timestamp(::swarm_msgs::msg::DroneState & msg)
  : msg_(msg)
  {}
  ::swarm_msgs::msg::DroneState timestamp(::swarm_msgs::msg::DroneState::_timestamp_type arg)
  {
    msg_.timestamp = std::move(arg);
    return std::move(msg_);
  }

private:
  ::swarm_msgs::msg::DroneState msg_;
};

class Init_DroneState_vz
{
public:
  explicit Init_DroneState_vz(::swarm_msgs::msg::DroneState & msg)
  : msg_(msg)
  {}
  Init_DroneState_timestamp vz(::swarm_msgs::msg::DroneState::_vz_type arg)
  {
    msg_.vz = std::move(arg);
    return Init_DroneState_timestamp(msg_);
  }

private:
  ::swarm_msgs::msg::DroneState msg_;
};

class Init_DroneState_vy
{
public:
  explicit Init_DroneState_vy(::swarm_msgs::msg::DroneState & msg)
  : msg_(msg)
  {}
  Init_DroneState_vz vy(::swarm_msgs::msg::DroneState::_vy_type arg)
  {
    msg_.vy = std::move(arg);
    return Init_DroneState_vz(msg_);
  }

private:
  ::swarm_msgs::msg::DroneState msg_;
};

class Init_DroneState_vx
{
public:
  explicit Init_DroneState_vx(::swarm_msgs::msg::DroneState & msg)
  : msg_(msg)
  {}
  Init_DroneState_vy vx(::swarm_msgs::msg::DroneState::_vx_type arg)
  {
    msg_.vx = std::move(arg);
    return Init_DroneState_vy(msg_);
  }

private:
  ::swarm_msgs::msg::DroneState msg_;
};

class Init_DroneState_z
{
public:
  explicit Init_DroneState_z(::swarm_msgs::msg::DroneState & msg)
  : msg_(msg)
  {}
  Init_DroneState_vx z(::swarm_msgs::msg::DroneState::_z_type arg)
  {
    msg_.z = std::move(arg);
    return Init_DroneState_vx(msg_);
  }

private:
  ::swarm_msgs::msg::DroneState msg_;
};

class Init_DroneState_y
{
public:
  explicit Init_DroneState_y(::swarm_msgs::msg::DroneState & msg)
  : msg_(msg)
  {}
  Init_DroneState_z y(::swarm_msgs::msg::DroneState::_y_type arg)
  {
    msg_.y = std::move(arg);
    return Init_DroneState_z(msg_);
  }

private:
  ::swarm_msgs::msg::DroneState msg_;
};

class Init_DroneState_x
{
public:
  explicit Init_DroneState_x(::swarm_msgs::msg::DroneState & msg)
  : msg_(msg)
  {}
  Init_DroneState_y x(::swarm_msgs::msg::DroneState::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_DroneState_y(msg_);
  }

private:
  ::swarm_msgs::msg::DroneState msg_;
};

class Init_DroneState_drone_id
{
public:
  Init_DroneState_drone_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_DroneState_x drone_id(::swarm_msgs::msg::DroneState::_drone_id_type arg)
  {
    msg_.drone_id = std::move(arg);
    return Init_DroneState_x(msg_);
  }

private:
  ::swarm_msgs::msg::DroneState msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::swarm_msgs::msg::DroneState>()
{
  return swarm_msgs::msg::builder::Init_DroneState_drone_id();
}

}  // namespace swarm_msgs

#endif  // SWARM_MSGS__MSG__DETAIL__DRONE_STATE__BUILDER_HPP_
