// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from swarm_msgs:msg/DroneState.idl
// generated code does not contain a copyright notice
#include "swarm_msgs/msg/detail/drone_state__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
swarm_msgs__msg__DroneState__init(swarm_msgs__msg__DroneState * msg)
{
  if (!msg) {
    return false;
  }
  // drone_id
  // x
  // y
  // z
  // vx
  // vy
  // vz
  // timestamp
  return true;
}

void
swarm_msgs__msg__DroneState__fini(swarm_msgs__msg__DroneState * msg)
{
  if (!msg) {
    return;
  }
  // drone_id
  // x
  // y
  // z
  // vx
  // vy
  // vz
  // timestamp
}

bool
swarm_msgs__msg__DroneState__are_equal(const swarm_msgs__msg__DroneState * lhs, const swarm_msgs__msg__DroneState * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // drone_id
  if (lhs->drone_id != rhs->drone_id) {
    return false;
  }
  // x
  if (lhs->x != rhs->x) {
    return false;
  }
  // y
  if (lhs->y != rhs->y) {
    return false;
  }
  // z
  if (lhs->z != rhs->z) {
    return false;
  }
  // vx
  if (lhs->vx != rhs->vx) {
    return false;
  }
  // vy
  if (lhs->vy != rhs->vy) {
    return false;
  }
  // vz
  if (lhs->vz != rhs->vz) {
    return false;
  }
  // timestamp
  if (lhs->timestamp != rhs->timestamp) {
    return false;
  }
  return true;
}

bool
swarm_msgs__msg__DroneState__copy(
  const swarm_msgs__msg__DroneState * input,
  swarm_msgs__msg__DroneState * output)
{
  if (!input || !output) {
    return false;
  }
  // drone_id
  output->drone_id = input->drone_id;
  // x
  output->x = input->x;
  // y
  output->y = input->y;
  // z
  output->z = input->z;
  // vx
  output->vx = input->vx;
  // vy
  output->vy = input->vy;
  // vz
  output->vz = input->vz;
  // timestamp
  output->timestamp = input->timestamp;
  return true;
}

swarm_msgs__msg__DroneState *
swarm_msgs__msg__DroneState__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  swarm_msgs__msg__DroneState * msg = (swarm_msgs__msg__DroneState *)allocator.allocate(sizeof(swarm_msgs__msg__DroneState), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(swarm_msgs__msg__DroneState));
  bool success = swarm_msgs__msg__DroneState__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
swarm_msgs__msg__DroneState__destroy(swarm_msgs__msg__DroneState * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    swarm_msgs__msg__DroneState__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
swarm_msgs__msg__DroneState__Sequence__init(swarm_msgs__msg__DroneState__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  swarm_msgs__msg__DroneState * data = NULL;

  if (size) {
    data = (swarm_msgs__msg__DroneState *)allocator.zero_allocate(size, sizeof(swarm_msgs__msg__DroneState), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = swarm_msgs__msg__DroneState__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        swarm_msgs__msg__DroneState__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
swarm_msgs__msg__DroneState__Sequence__fini(swarm_msgs__msg__DroneState__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      swarm_msgs__msg__DroneState__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

swarm_msgs__msg__DroneState__Sequence *
swarm_msgs__msg__DroneState__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  swarm_msgs__msg__DroneState__Sequence * array = (swarm_msgs__msg__DroneState__Sequence *)allocator.allocate(sizeof(swarm_msgs__msg__DroneState__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = swarm_msgs__msg__DroneState__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
swarm_msgs__msg__DroneState__Sequence__destroy(swarm_msgs__msg__DroneState__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    swarm_msgs__msg__DroneState__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
swarm_msgs__msg__DroneState__Sequence__are_equal(const swarm_msgs__msg__DroneState__Sequence * lhs, const swarm_msgs__msg__DroneState__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!swarm_msgs__msg__DroneState__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
swarm_msgs__msg__DroneState__Sequence__copy(
  const swarm_msgs__msg__DroneState__Sequence * input,
  swarm_msgs__msg__DroneState__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(swarm_msgs__msg__DroneState);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    swarm_msgs__msg__DroneState * data =
      (swarm_msgs__msg__DroneState *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!swarm_msgs__msg__DroneState__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          swarm_msgs__msg__DroneState__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!swarm_msgs__msg__DroneState__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
