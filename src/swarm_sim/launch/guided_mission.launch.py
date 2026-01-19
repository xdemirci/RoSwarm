from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    # Declare arguments
    num_drones_arg = DeclareLaunchArgument(
        'num_drones',
        default_value='3',
        description='Number of drones in the swarm'
    )
    
    num_drones = LaunchConfiguration('num_drones')
    
    # We'll create 3 drones at different starting positions
    drone_configs = [
        {'id': 1, 'x': 0.0, 'y': 0.0, 'z': 0.0},
        {'id': 2, 'x': 10.0, 'y': 0.0, 'z': 0.0},
        {'id': 3, 'x': 0.0, 'y': 10.0, 'z': 0.0},
    ]
    
    nodes = []
    
    # Launch simulated drones and mission controllers
    for config in drone_configs:
        # Simulated drone
        nodes.append(Node(
            package='swarm_sim',
            executable='simulated_drone',
            name=f'simulated_drone_{config["id"]}',
            parameters=[{
                'drone_id': config['id'],
                'start_x': config['x'],
                'start_y': config['y'],
                'start_z': config['z'],
            }],
            output='screen'
        ))
        
        # Mission controller for each drone
        nodes.append(Node(
            package='swarm_sim',
            executable='mission_controller',
            name=f'mission_controller_{config["id"]}',
            parameters=[{
                'drone_id': config['id'],
            }],
            output='screen'
        ))
    
    # Visualizer
    nodes.append(Node(
        package='swarm_sim',
        executable='visualizer',
        name='visualizer',
        parameters=[{'num_drones': 3}],
        output='screen'
    ))
    
    return LaunchDescription([
        num_drones_arg,
        *nodes
    ])
