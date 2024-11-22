import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument

def generate_launch_description():
    # Path
    waypoint_xml_default = os.path.join(
        get_package_share_directory('guenbot2_waypoint'),
        'waypoint_xml',
        'guen_qrcode.xml'
    )

    # Parameters
    declare_waypoint_xml = DeclareLaunchArgument(
        'waypoint_xml',
        default_value=waypoint_xml_default,
        description='Path to the waypoint XML file'
    )

    # Behavior Tree Node
    behavior_tree = Node(
        package='guenbot2_waypoint',
        executable='guenbot2_waypoint',
        parameters=[{'waypoint_xml': LaunchConfiguration('waypoint_xml')}],
        output='screen'
    )

    # ZBar Node
    zbar_node = Node(
        package='zbar_ros',
        executable='barcode_reader',
        name='zbar_node',
        remappings=[
            ('/image', '/camera/image_raw'),
            ('/barcode_data', '/qr_code_data')
        ],
        output='screen'
    )


    # Launch Description
    ld = LaunchDescription()
    ld.add_action(declare_waypoint_xml)
    ld.add_action(behavior_tree)
    ld.add_action(zbar_node)
    return ld
