#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from swarm_msgs.msg import DroneState
from geometry_msgs.msg import TwistStamped
import numpy as np
from collections import defaultdict
import time

class SwarmCoordinator(Node):
    def __init__(self):
        super().__init__('swarm_coordinator')
        
        self.declare_parameter('drone_id', 1)
        self.declare_parameter('num_drones', 3)
        self.declare_parameter('separation_distance', 5.0)
        
        self.drone_id = self.get_parameter('drone_id').value
        self.num_drones = self.get_parameter('num_drones').value
        self.sep_dist = self.get_parameter('separation_distance').value
        
        self.cmd_vel_pub = self.create_publisher(
            TwistStamped, f'drone_{self.drone_id}/cmd_velocity', 10)
        
        self.state_subs = []
        for i in range(1, self.num_drones + 1):
            sub = self.create_subscription(
                DroneState, f'drone_{i}/state', 
                self.state_callback, 10)
            self.state_subs.append(sub)
        
        self.swarm_states = {}
        self.last_update = defaultdict(float)
        
        self.create_timer(0.2, self.compute_swarm_control)
        
        self.K_SEP = 2.0
        self.K_COH = 0.5
        self.K_ALI = 1.0
        self.MAX_VEL = 3.0
        self.TIMEOUT = 2.0
        
        self.get_logger().info(f'Coordinator for Drone {self.drone_id} started')
    
    def state_callback(self, msg):
        self.swarm_states[msg.drone_id] = msg
        self.last_update[msg.drone_id] = time.time()
    
    def get_active_neighbors(self):
        current_time = time.time()
        active = {}
        for drone_id, state in self.swarm_states.items():
            if drone_id != self.drone_id:
                if current_time - self.last_update[drone_id] < self.TIMEOUT:
                    active[drone_id] = state
        return active
    
    def compute_swarm_control(self):
        if self.drone_id not in self.swarm_states:
            return
        
        neighbors = self.get_active_neighbors()
        if not neighbors:
            self.get_logger().warn('No neighbors detected!', throttle_duration_sec=2.0)
            return
        
        my_state = self.swarm_states[self.drone_id]
        my_pos = np.array([my_state.x, my_state.y, my_state.z])
        my_vel = np.array([my_state.vx, my_state.vy, my_state.vz])
        
        sep_force = np.zeros(3)
        coh_force = np.zeros(3)
        ali_force = np.zeros(3)
        
        for neighbor_id, neighbor in neighbors.items():
            n_pos = np.array([neighbor.x, neighbor.y, neighbor.z])
            n_vel = np.array([neighbor.vx, neighbor.vy, neighbor.vz])
            
            diff = n_pos - my_pos
            distance = np.linalg.norm(diff)
            
            if distance > 0:
                if distance < self.sep_dist:
                    sep_force -= diff / (distance ** 2)
                
                coh_force += diff
                ali_force += n_vel - my_vel
        
        if len(neighbors) > 0:
            coh_force /= len(neighbors)
            ali_force /= len(neighbors)
        
        control = (self.K_SEP * sep_force + 
                   self.K_COH * coh_force + 
                   self.K_ALI * ali_force)
        
        speed = np.linalg.norm(control)
        if speed > self.MAX_VEL:
            control = control * (self.MAX_VEL / speed)
        
        cmd = TwistStamped()
        cmd.header.stamp = self.get_clock().now().to_msg()
        cmd.twist.linear.x = float(control[0])
        cmd.twist.linear.y = float(control[1])
        cmd.twist.linear.z = float(control[2])
        
        self.cmd_vel_pub.publish(cmd)
        
        self.get_logger().info(
            f'D{self.drone_id}: Neighbors={len(neighbors)}, '
            f'Pos=[{my_pos[0]:.1f},{my_pos[1]:.1f},{my_pos[2]:.1f}], '
            f'Cmd=[{control[0]:.2f},{control[1]:.2f},{control[2]:.2f}]',
            throttle_duration_sec=1.0
        )

def main(args=None):
    rclpy.init(args=args)
    node = SwarmCoordinator()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
