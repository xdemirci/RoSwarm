#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from swarm_msgs.msg import DroneState
from geometry_msgs.msg import TwistStamped
from std_msgs.msg import String
import numpy as np
import json

class MissionController(Node):
    def __init__(self):
        super().__init__('mission_controller')
        
        self.declare_parameter('drone_id', 1)
        self.drone_id = self.get_parameter('drone_id').value
        
        # Publishers
        self.cmd_vel_pub = self.create_publisher(
            TwistStamped, f'drone_{self.drone_id}/cmd_velocity', 10)
        
        self.status_pub = self.create_publisher(
            String, f'drone_{self.drone_id}/mission_status', 10)
        
        # Subscribers
        self.state_sub = self.create_subscription(
            DroneState, f'drone_{self.drone_id}/state', 
            self.state_callback, 10)
        
        self.mission_sub = self.create_subscription(
            String, f'drone_{self.drone_id}/mission_cmd',
            self.mission_callback, 10)
        
        # State variables
        self.current_state = None
        self.armed = False
        self.mission_mode = 'IDLE'  # IDLE, ARMING, TAKEOFF, GOTO, LANDING, HOVER
        self.target_position = None
        self.target_altitude = 10.0
        self.position_threshold = 0.5  # meters
        self.velocity_threshold = 0.2  # m/s
        
        # Control gains
        self.K_P = 1.5  # Position gain
        self.K_D = 0.8  # Velocity damping
        self.MAX_VEL = 5.0
        self.MAX_CLIMB_RATE = 2.0
        
        self.create_timer(0.1, self.control_loop)
        
        self.get_logger().info(f'Mission Controller for Drone {self.drone_id} started')
    
    def state_callback(self, msg):
        self.current_state = msg
    
    def mission_callback(self, msg):
        """Handle mission commands via JSON strings"""
        try:
            cmd = json.loads(msg.data)
            command = cmd.get('command', '').upper()
            
            if command == 'ARM':
                self.arm()
            elif command == 'DISARM':
                self.disarm()
            elif command == 'TAKEOFF':
                altitude = cmd.get('altitude', 10.0)
                self.takeoff(altitude)
            elif command == 'GOTO':
                x = cmd.get('x', 0.0)
                y = cmd.get('y', 0.0)
                z = cmd.get('z', self.target_altitude)
                self.goto(x, y, z)
            elif command == 'LAND':
                self.land()
            elif command == 'HOVER':
                self.hover()
            elif command == 'RTL':  # Return to launch
                self.return_to_launch()
            else:
                self.get_logger().warn(f'Unknown command: {command}')
                
        except json.JSONDecodeError:
            self.get_logger().error(f'Invalid JSON command: {msg.data}')
    
    def arm(self):
        """Arm the drone"""
        if not self.armed:
            self.armed = True
            self.mission_mode = 'ARMED'
            self.get_logger().info(f'Drone {self.drone_id} ARMED')
            self.publish_status('ARMED')
    
    def disarm(self):
        """Disarm the drone"""
        if self.armed:
            self.armed = False
            self.mission_mode = 'IDLE'
            self.get_logger().info(f'Drone {self.drone_id} DISARMED')
            self.publish_status('DISARMED')
    
    def takeoff(self, altitude):
        """Takeoff to specified altitude"""
        if not self.armed:
            self.get_logger().warn('Cannot takeoff - drone not armed!')
            return
        
        self.target_altitude = altitude
        if self.current_state:
            self.target_position = np.array([
                self.current_state.x,
                self.current_state.y,
                altitude
            ])
        else:
            self.target_position = np.array([0.0, 0.0, altitude])
        
        self.mission_mode = 'TAKEOFF'
        self.get_logger().info(f'Drone {self.drone_id} taking off to {altitude}m')
        self.publish_status(f'TAKEOFF to {altitude}m')
    
    def goto(self, x, y, z):
        """Fly to specified position"""
        if not self.armed:
            self.get_logger().warn('Cannot goto - drone not armed!')
            return
        
        self.target_position = np.array([x, y, z])
        self.mission_mode = 'GOTO'
        self.get_logger().info(f'Drone {self.drone_id} going to [{x:.1f}, {y:.1f}, {z:.1f}]')
        self.publish_status(f'GOTO [{x:.1f}, {y:.1f}, {z:.1f}]')
    
    def land(self):
        """Land the drone"""
        if not self.armed:
            self.get_logger().warn('Cannot land - drone not armed!')
            return
        
        if self.current_state:
            self.target_position = np.array([
                self.current_state.x,
                self.current_state.y,
                0.0
            ])
        
        self.mission_mode = 'LANDING'
        self.get_logger().info(f'Drone {self.drone_id} landing')
        self.publish_status('LANDING')
    
    def hover(self):
        """Hover at current position"""
        if not self.armed:
            self.get_logger().warn('Cannot hover - drone not armed!')
            return
        
        if self.current_state:
            self.target_position = np.array([
                self.current_state.x,
                self.current_state.y,
                self.current_state.z
            ])
        
        self.mission_mode = 'HOVER'
        self.get_logger().info(f'Drone {self.drone_id} hovering')
        self.publish_status('HOVER')
    
    def return_to_launch(self):
        """Return to launch position and land"""
        if not self.armed:
            self.get_logger().warn('Cannot RTL - drone not armed!')
            return
        
        # Return to origin
        self.target_position = np.array([0.0, 0.0, self.target_altitude])
        self.mission_mode = 'RTL'
        self.get_logger().info(f'Drone {self.drone_id} returning to launch')
        self.publish_status('RTL')
    
    def control_loop(self):
        """Main control loop"""
        if not self.armed or self.current_state is None:
            # Send zero velocity when not armed
            self.publish_velocity(0.0, 0.0, 0.0)
            return
        
        if self.target_position is None:
            return
        
        # Current position and velocity
        current_pos = np.array([
            self.current_state.x,
            self.current_state.y,
            self.current_state.z
        ])
        current_vel = np.array([
            self.current_state.vx,
            self.current_state.vy,
            self.current_state.vz
        ])
        
        # Position error
        error = self.target_position - current_pos
        distance = np.linalg.norm(error)
        
        # Check if reached target
        velocity_mag = np.linalg.norm(current_vel)
        if distance < self.position_threshold and velocity_mag < self.velocity_threshold:
            if self.mission_mode == 'TAKEOFF':
                self.get_logger().info(f'Drone {self.drone_id} reached takeoff altitude')
                self.hover()
            elif self.mission_mode == 'GOTO':
                self.get_logger().info(f'Drone {self.drone_id} reached target position')
                self.hover()
            elif self.mission_mode == 'LANDING':
                if self.current_state.z < 0.2:
                    self.get_logger().info(f'Drone {self.drone_id} landed')
                    self.disarm()
                    return
            elif self.mission_mode == 'RTL':
                self.get_logger().info(f'Drone {self.drone_id} reached launch point, landing')
                self.land()
        
        # PD controller
        control_vel = self.K_P * error - self.K_D * current_vel
        
        # Limit climb rate for takeoff and landing
        if self.mission_mode == 'TAKEOFF' or self.mission_mode == 'LANDING':
            control_vel[2] = np.clip(control_vel[2], -self.MAX_CLIMB_RATE, self.MAX_CLIMB_RATE)
        
        # Limit maximum velocity
        speed = np.linalg.norm(control_vel)
        if speed > self.MAX_VEL:
            control_vel = control_vel * (self.MAX_VEL / speed)
        
        # Publish velocity command
        self.publish_velocity(control_vel[0], control_vel[1], control_vel[2])
        
        # Log status periodically
        if self.get_clock().now().nanoseconds % 1000000000 < 100000000:  # Every ~1 second
            self.get_logger().info(
                f'D{self.drone_id} [{self.mission_mode}]: '
                f'Pos=[{current_pos[0]:.1f},{current_pos[1]:.1f},{current_pos[2]:.1f}], '
                f'Target=[{self.target_position[0]:.1f},{self.target_position[1]:.1f},{self.target_position[2]:.1f}], '
                f'Dist={distance:.2f}m'
            )
    
    def publish_velocity(self, vx, vy, vz):
        """Publish velocity command"""
        cmd = TwistStamped()
        cmd.header.stamp = self.get_clock().now().to_msg()
        cmd.twist.linear.x = float(vx)
        cmd.twist.linear.y = float(vy)
        cmd.twist.linear.z = float(vz)
        self.cmd_vel_pub.publish(cmd)
    
    def publish_status(self, status):
        """Publish mission status"""
        msg = String()
        msg.data = f'{{"drone_id": {self.drone_id}, "status": "{status}"}}'
        self.status_pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = MissionController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
