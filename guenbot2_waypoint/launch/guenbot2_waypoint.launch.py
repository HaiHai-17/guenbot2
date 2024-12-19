import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch_ros.actions.node import Node

def generate_launch_description():
    # Path
    waypoint_xml_dir = os.path.join(get_package_share_directory('guenbot2_waypoint'), 'waypoint_xml')

    # Parameters
    waypoint_xml = LaunchConfiguration('waypoint_xml', default=waypoint_xml_dir+'/guen_nav_mememan.xml')

    behavior_tree = Node(
        package='guenbot2_waypoint',
        executable='guenbot2_waypoint',
        parameters=[{'waypoint_xml': waypoint_xml}],
        output='screen'
    )

    ld = LaunchDescription()
    ld.add_action(behavior_tree)
    return ld
