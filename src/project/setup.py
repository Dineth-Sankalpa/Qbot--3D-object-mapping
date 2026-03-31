from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'project'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
    ],
    
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='netrunner',
    maintainer_email='dinethsankalpaofficial@gmail.com',
    description='Project package for ROS 2',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'qbot_controller = project.qbot_controller:main',
            'navigation_server = project.navigation_server:main',
            'circular_scanner = qbot_kinematics.circular_scanner:main',
            
        ],
    },
)