from setuptools import setup
import os
from glob import glob

package_name = 'swarm_sim'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='you@example.com',
    description='Swarm simulation',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'simulated_drone = swarm_sim.simulated_drone:main',
            'swarm_coordinator = swarm_sim.swarm_coordinator:main',
            'visualizer = swarm_sim.visualizer:main',
            'mission_controller = swarm_sim.mission_controller:main',
            'mission_commander = swarm_sim.mission_commander:main',
            'mavlink_bridge = swarm_sim.mavlink_bridge:main'
        ],
    },
)

#
