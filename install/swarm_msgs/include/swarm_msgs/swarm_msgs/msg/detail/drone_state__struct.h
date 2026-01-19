// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from swarm_msgs:msg/DroneState.idl
// generated code does not contain a copyright notice

#ifndef SWARM_MSGS__MSG__DETAIL__DRONE_STATE__STRUCT_H_
#define SWARM_MSGS__MSG__DETAIL__DRONE_STATE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/DroneState in the package swarm_msgs.
typedef struct swarm_msgs__msg__DroneState
{
  uint8_t drone_id;
  double x;
  double y;
  double z;
  double vx;
  double vy;
  double vz;
  uint64_t timestamp;
} swarm_msgs__msg__DroneState;

// Struct for a sequence of swarm_msgs__msg__DroneState.
typedef struct swarm_msgs__msg__DroneState__Sequence
{
  swarm_msgs__msg__DroneState * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} swarm_msgs__msg__DroneState__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SWARM_MSGS__MSG__DETAIL__DRONE_STATE__STRUCT_H_
