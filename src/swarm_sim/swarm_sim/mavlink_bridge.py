#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from swarm_msgs.msg import DroneState
from std_msgs.msg import String
import socket
import struct
import time
import json

class MAVLinkBridge(Node):
    """
    Bridges ROS2 simulation to MAVLink protocol for MAVProxy monitoring
    """
    def __init__(self):
        super().__init__('mavlink_bridge')
        
        self.declare_parameter('drone_id', 1)
        self.declare_parameter('mavlink_port', 14550)  # Default MAVLink UDP port
        self.declare_parameter('gcs_ip', '127.0.0.1')  # Ground Control Station IP
        self.declare_parameter('system_id', 1)  # MAVLink system ID
        
        self.drone_id = self.get_parameter('drone_id').value
        self.mavlink_port = self.get_parameter('mavlink_port').value
        self.gcs_ip = self.get_parameter('gcs_ip').value
        self.system_id = self.get_parameter('system_id').value
        
        # Create UDP socket for MAVLink
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('', self.mavlink_port))
        self.gcs_address = (self.gcs_ip, 14550)
        
        # Subscribe to drone state and mission status
        self.state_sub = self.create_subscription(
            DroneState, f'drone_{self.drone_id}/state',
            self.state_callback, 10)
        
        self.status_sub = self.create_subscription(
            String, f'drone_{self.drone_id}/mission_status',
            self.status_callback, 10)
        
        # MAVLink state
        self.current_state = None
        self.armed = False
        self.mode = "STABILIZE"
        self.base_mode = 81  # MAV_MODE_FLAG_CUSTOM_MODE_ENABLED | MAV_MODE_FLAG_STABILIZE_ENABLED
        self.custom_mode = 0
        self.system_status = 3  # MAV_STATE_STANDBY
        
        # Heartbeat timer (1Hz)
        self.create_timer(1.0, self.send_heartbeat)
        
        # Position update timer (10Hz)
        self.create_timer(0.1, self.send_position)
        
        # GPS timer (5Hz)
        self.create_timer(0.2, self.send_gps)
        
        # Attitude timer (10Hz)
        self.create_timer(0.1, self.send_attitude)
        
        # VFR HUD timer (4Hz)
        self.create_timer(0.25, self.send_vfr_hud)
        
        # Home position (for reference)
        self.home_lat = 0
        self.home_lon = 0
        self.home_alt = 0
        
        self.get_logger().info(f'MAVLink Bridge started for Drone {self.drone_id}')
        self.get_logger().info(f'Broadcasting on UDP port {self.mavlink_port}')
    
    def state_callback(self, msg):
        """Update current state from ROS2"""
        self.current_state = msg
    
    def status_callback(self, msg):
        """Update armed/mode status from mission controller"""
        try:
            data = json.loads(msg.data)
            status = data.get('status', '')
            
            if 'ARMED' in status:
                self.armed = True
                self.system_status = 4  # MAV_STATE_ACTIVE
            elif 'DISARMED' in status:
                self.armed = False
                self.system_status = 3  # MAV_STATE_STANDBY
            
            if 'TAKEOFF' in status:
                self.mode = "GUIDED"
                self.custom_mode = 4
            elif 'LAND' in status:
                self.mode = "LAND"
                self.custom_mode = 9
            elif 'HOVER' in status or 'GOTO' in status:
                self.mode = "GUIDED"
                self.custom_mode = 4
            elif 'RTL' in status:
                self.mode = "RTL"
                self.custom_mode = 6
                
        except Exception as e:
            self.get_logger().warn(f'Error parsing status: {e}')
    
    def send_mavlink_message(self, msg_id, payload):
        """Send a MAVLink 1.0 message"""
        # MAVLink 1.0 format
        STX = 0xFE
        seq = int(time.time() * 1000) % 256
        sysid = self.system_id
        compid = 1  # MAV_COMP_ID_AUTOPILOT1
        
        # Create packet
        packet = struct.pack('<BBBBBB',
            STX,           # Start byte
            len(payload),  # Payload length
            seq,           # Sequence
            sysid,         # System ID
            compid,        # Component ID
            msg_id         # Message ID
        )
        
        packet += payload
        
        # Calculate checksum
        crc = self.crc_calculate(packet[1:], msg_id)
        packet += struct.pack('<H', crc)
        
        # Send to GCS
        try:
            self.sock.sendto(packet, self.gcs_address)
        except Exception as e:
            self.get_logger().warn(f'Failed to send MAVLink: {e}', throttle_duration_sec=5.0)
    
    def crc_calculate(self, data, msg_id):
        """Calculate MAVLink CRC"""
        # CRC extra values for common messages
        crc_extra = {
            0: 50,   # HEARTBEAT
            24: 24,  # GPS_RAW_INT
            30: 39,  # ATTITUDE
            32: 185, # LOCAL_POSITION_NED
            33: 104, # GLOBAL_POSITION_INT
            74: 20,  # VFR_HUD
        }
        
        crc = 0xFFFF
        for byte in data:
            tmp = byte ^ (crc & 0xFF)
            tmp ^= (tmp << 4) & 0xFF
            crc = (crc >> 8) ^ (tmp << 8) ^ (tmp << 3) ^ (tmp >> 4)
        
        # Add CRC_EXTRA
        if msg_id in crc_extra:
            tmp = crc_extra[msg_id] ^ (crc & 0xFF)
            tmp ^= (tmp << 4) & 0xFF
            crc = (crc >> 8) ^ (tmp << 8) ^ (tmp << 3) ^ (tmp >> 4)
        
        return crc & 0xFFFF
    
    def send_heartbeat(self):
        """Send HEARTBEAT (ID=0)"""
        base_mode = self.base_mode
        if self.armed:
            base_mode |= 128  # MAV_MODE_FLAG_SAFETY_ARMED
        
        payload = struct.pack('<IBBBBB',
            self.custom_mode,      # custom_mode
            2,                     # type (MAV_TYPE_QUADROTOR)
            8,                     # autopilot (MAV_AUTOPILOT_INVALID)
            base_mode,             # base_mode
            self.system_status,    # system_status
            3                      # mavlink_version
        )
        
        self.send_mavlink_message(0, payload)
    
    def send_position(self):
        """Send LOCAL_POSITION_NED (ID=32)"""
        if self.current_state is None:
            return
        
        payload = struct.pack('<Iffffffff',
            int(time.time() * 1000) % (2**32),  # time_boot_ms
            float(self.current_state.x),        # x (North)
            float(self.current_state.y),        # y (East)
            float(-self.current_state.z),       # z (Down - NED convention)
            float(self.current_state.vx),       # vx
            float(self.current_state.vy),       # vy
            float(-self.current_state.vz)       # vz
        )
        
        self.send_mavlink_message(32, payload)
    
    def send_gps(self):
        """Send GPS_RAW_INT (ID=24)"""
        if self.current_state is None:
            return
        
        # Convert local coordinates to fake GPS (very rough)
        # 1 degree latitude ≈ 111km
        lat = int((self.home_lat + (self.current_state.x / 111000.0)) * 1e7)
        lon = int((self.home_lon + (self.current_state.y / 111000.0)) * 1e7)
        alt = int(self.current_state.z * 1000)  # mm
        
        payload = struct.pack('<QbBiiiiHHHHB',
            int(time.time() * 1e6) % (2**64),  # time_usec
            3,                                  # fix_type (3D fix)
            lat,                                # lat
            lon,                                # lon
            alt,                                # alt (mm)
            65535,                              # eph (unknown)
            65535,                              # epv (unknown)
            0,                                  # vel (cm/s)
            0,                                  # cog (centidegrees)
            10                                  # satellites_visible
        )
        
        self.send_mavlink_message(24, payload)
    
    def send_attitude(self):
        """Send ATTITUDE (ID=30)"""
        if self.current_state is None:
            return
        
        payload = struct.pack('<Iffffff',
            int(time.time() * 1000) % (2**32),  # time_boot_ms
            0.0,                                 # roll
            0.0,                                 # pitch
            0.0,                                 # yaw
            0.0,                                 # rollspeed
            0.0,                                 # pitchspeed
            0.0                                  # yawspeed
        )
        
        self.send_mavlink_message(30, payload)
    
    def send_vfr_hud(self):
        """Send VFR_HUD (ID=74) - shows in MAVProxy"""
        if self.current_state is None:
            return
        
        import math
        
        # Calculate ground speed
        groundspeed = math.sqrt(
            self.current_state.vx**2 + 
            self.current_state.vy**2
        )
        
        # Calculate heading from velocity
        heading = math.degrees(math.atan2(
            self.current_state.vy,
            self.current_state.vx
        )) % 360
        
        payload = struct.pack('<fffffHh',
            float(groundspeed),              # airspeed (m/s)
            float(groundspeed),              # groundspeed (m/s)
            int(heading),                    # heading (degrees)
            0,                               # throttle (%)
            float(self.current_state.z),     # alt (m)
            float(-self.current_state.vz)    # climb (m/s)
        )
        
        self.send_mavlink_message(74, payload)
    
    def send_global_position(self):
        """Send GLOBAL_POSITION_INT (ID=33)"""
        if self.current_state is None:
            return
        
        # Similar to GPS but includes velocities
        lat = int((self.home_lat + (self.current_state.x / 111000.0)) * 1e7)
        lon = int((self.home_lon + (self.current_state.y / 111000.0)) * 1e7)
        alt = int(self.current_state.z * 1000)  # mm
        
        payload = struct.pack('<Iiiiihhhh',
            int(time.time() * 1000) % (2**32),        # time_boot_ms
            lat,                                       # lat
            lon,                                       # lon
            alt,                                       # alt (mm MSL)
            int(self.current_state.z * 1000),         # relative_alt (mm)
            int(self.current_state.vx * 100),         # vx (cm/s)
            int(self.current_state.vy * 100),         # vy (cm/s)
            int(self.current_state.vz * 100),         # vz (cm/s)
            0                                          # hdg (centidegrees)
        )
        
        self.send_mavlink_message(33, payload)

def main(args=None):
    rclpy.init(args=args)
    node = MAVLinkBridge()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
