#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from swarm_msgs.msg import DroneState
from geometry_msgs.msg import TwistStamped
import numpy as np
import time

class SimulatedDrone(Node):
    def __init__(self):
        super().__init__('simulated_drone')
        
        self.declare_parameter('drone_id', 1)
        self.declare_parameter('start_x', 0.0)
        self.declare_parameter('start_y', 0.0)
        self.declare_parameter('start_z', 10.0)
        
        self.drone_id = self.get_parameter('drone_id').value
        
        self.pos = np.array([
            self.get_parameter('start_x').value,
            self.get_parameter('start_y').value,
            self.get_parameter('start_z').value
        ])
        self.vel = np.zeros(3)
        self.cmd_vel = np.zeros(3)
        
        self.state_pub = self.create_publisher(
            DroneState, f'drone_{self.drone_id}/state', 10)
        
        self.cmd_sub = self.create_subscription(
            TwistStamped, f'drone_{self.drone_id}/cmd_velocity', 
            self.cmd_callback, 10)
        
        self.dt = 0.05
        self.create_timer(self.dt, self.simulate_physics)
        self.create_timer(0.1, self.publish_state)
        
        self.get_logger().info(f'Drone {self.drone_id} spawned at {self.pos}')
    
    def cmd_callback(self, msg):
        self.cmd_vel = np.array([
            msg.twist.linear.x,
            msg.twist.linear.y,
            msg.twist.linear.z
        ])
    
    def simulate_physics(self):
        gain = 0.3
        self.vel += (self.cmd_vel - self.vel) * gain
        self.pos += self.vel * self.dt
        
        if self.pos[2] < 0:
            self.pos[2] = 0
            self.vel[2] = 0
    
    def publish_state(self):
        state = DroneState()
        state.drone_id = self.drone_id
        state.x = self.pos[0]
        state.y = self.pos[1]
        state.z = self.pos[2]
        state.vx = self.vel[0]
        state.vy = self.vel[1]
        state.vz = self.vel[2]
        state.timestamp = int(time.time() * 1e6)
        
        self.state_pub.publish(state)

def main(args=None):
    rclpy.init(args=args)
    node = SimulatedDrone()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
