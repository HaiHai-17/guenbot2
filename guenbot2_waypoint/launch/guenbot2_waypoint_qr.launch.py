import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    # Path
    waypoint_xml_dir = os.path.join(get_package_share_directory('guenbot2_waypoint'), 'waypoint_xml')

    # Parameters
    waypoint_xml = LaunchConfiguration('waypoint_xml', default=waypoint_xml_dir+'/guen_nav_mememan.xml')

    # Nodes
    behavior_tree = Node(
        package='guenbot2_waypoint',
        executable='guenbot2_waypoint',
        parameters=[{'waypoint_xml': waypoint_xml}],
        output='screen'
    )

    camera_node = Node(
        package='v4l2_camera',
        executable='v4l2_camera_node',
        name='camera',
        output='screen',
        parameters=[{'video_device': '/dev/video0'}]
    )

    barcode_node = Node(
        package='zbar_ros',
        executable='barcode_reader',
        name='barcode_reader',
        output='screen',
        remappings=[('/barcode', '/barcode')]
    )

    qr_navigation_node = Node(
        package='guenbot2_waypoint',
        executable='qr_navigation',
        name='qr_navigation',
        output='screen'
    )

    # Launch description
    ld = LaunchDescription()
    ld.add_action(behavior_tree)
    ld.add_action(camera_node)
    ld.add_action(barcode_node)
    ld.add_action(qr_navigation_node)

    return ld