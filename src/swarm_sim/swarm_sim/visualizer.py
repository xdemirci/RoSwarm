#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from swarm_msgs.msg import DroneState
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from collections import defaultdict

class SwarmVisualizer(Node):
    def __init__(self):
        super().__init__('swarm_visualizer')
        
        self.declare_parameter('num_drones', 3)
        self.num_drones = self.get_parameter('num_drones').value
        
        self.state_subs = []
        for i in range(1, self.num_drones + 1):
            sub = self.create_subscription(
                DroneState, f'drone_{i}/state', 
                self.state_callback, 10)
            self.state_subs.append(sub)
        
        self.positions = defaultdict(lambda: np.zeros(3))
        self.velocities = defaultdict(lambda: np.zeros(3))
        
        plt.ion()
        self.fig = plt.figure(figsize=(12, 8))
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        self.create_timer(0.2, self.update_plot)
        
        self.get_logger().info('Visualizer started')
    
    def state_callback(self, msg):
        self.positions[msg.drone_id] = np.array([msg.x, msg.y, msg.z])
        self.velocities[msg.drone_id] = np.array([msg.vx, msg.vy, msg.vz])
    
    def update_plot(self):
        if not self.positions:
            return
        
        self.ax.clear()
        
        for drone_id, pos in self.positions.items():
            self.ax.scatter(pos[0], pos[1], pos[2], 
                          s=200, c=f'C{drone_id-1}', marker='o', 
                          label=f'Drone {drone_id}')
            
            vel = self.velocities[drone_id]
            if np.linalg.norm(vel) > 0.1:
                self.ax.quiver(pos[0], pos[1], pos[2],
                             vel[0], vel[1], vel[2],
                             color=f'C{drone_id-1}', alpha=0.6,
                             length=2.0, normalize=True, arrow_length_ratio=0.3)
        
        positions_array = np.array(list(self.positions.values()))
        com = positions_array.mean(axis=0)
        
        self.ax.set_xlabel('X (m)')
        self.ax.set_ylabel('Y (m)')
        self.ax.set_zlabel('Z (m)')
        self.ax.set_title(f'Swarm Simulation - {len(self.positions)} Drones')
        
        max_range = 20
        self.ax.set_xlim([com[0] - max_range, com[0] + max_range])
        self.ax.set_ylim([com[1] - max_range, com[1] + max_range])
        self.ax.set_zlim([0, 20])
        
        self.ax.legend()
        self.ax.grid(True)
        
        plt.draw()
        plt.pause(0.001)

def main(args=None):
    rclpy.init(args=args)
    node = SwarmVisualizer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
