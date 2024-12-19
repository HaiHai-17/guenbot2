import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, GroupAction
from launch.substitutions import PathJoinSubstitution, PythonExpression
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare
from launch.conditions import IfCondition
from launch_ros.actions import Node, SetRemap


def generate_launch_description():
    laser_sensor_name = os.getenv('GUENBOT2_LASER_SENSOR', '')
    # depth_sensor_name = os.getenv('GUENBOT2_DEPTH_SENSOR', '')
    
    fake_laser_config_path = PathJoinSubstitution(
        [FindPackageShare('guenbot2_bringup'), 'config', 'fake_laser.yaml']
    )

    #indices
    #0 - depth topic (str)
    #1 - depth info topic (str)
    # depth_topics = {
    #     '': ['', '', '', {}, '', ''],
    #     'realsense': ['/camera/depth/image_rect_raw', '/camera/depth/camera_info'],
    #     'astra': ['/depth/rgb/ir', '/camera_info'],
    #     'zed': ['/zed/depth/depth_registered', '/zed/depth/camera_info'],
    #     'zed2': ['/zed/depth/depth_registered', '/zed/depth/camera_info'],
    #     'zed2i': ['/zed/depth/depth_registered', '/zed/depth/camera_info'],
    #     'zedm': ['/zed/depth/depth_registered', '/zed/depth/camera_info'],
    #     'oakd': ['/right/image_rect', '/right/camera_info'],
    #     'oakdlite': ['/right/image_rect', '/right/camera_info'],
    #     'oakdpro': ['/right/image_rect', '/right/camera_info'],
    # }

    # point_cloud_topics = {
    #     '': '',
    #     'realsense': '/camera/depth/color/points',
    #     'astra': '/camera/depth/points',
    #     'zed': '/zed/point_cloud/cloud_registered',
    #     'zed2': '/zed/point_cloud/cloud_registered',
    #     'zed2i': '/zed/point_cloud/cloud_registered',
    #     'zedm': '/zed/point_cloud/cloud_registered',
    #     'oakd': '/stereo/points',
    #     'oakdlite': '/stereo/points',
    #     'oakdpro': '/stereo/points',
    # }

    laser_launch_path = PathJoinSubstitution(
        [FindPackageShare('guenbot2_bringup'), 'launch', 'lasers.launch.py']
    )

    # depth_launch_path = PathJoinSubstitution(
    #     [FindPackageShare('guenbot2_bringup'), 'launch', 'depth.launch.py']
    # )

    return LaunchDescription([
        # GroupAction(
        #     actions=[
        #         SetRemap(src=point_cloud_topics[depth_sensor_name], dst='/camera/depth/color/points'),
        #         IncludeLaunchDescription(
        #             PythonLaunchDescriptionSource(depth_launch_path),
        #             condition=IfCondition(PythonExpression(['"" != "', depth_sensor_name, '"'])),
        #             launch_arguments={'sensor': depth_sensor_name}.items()   
        #         )
        #     ]
        # ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(laser_launch_path),
            condition=IfCondition(PythonExpression(['"" != "', laser_sensor_name, '"'])),
            launch_arguments={
                'sensor': laser_sensor_name
            }.items()   
        ),
        # Node(
        #     condition=IfCondition(PythonExpression(['"" != "', laser_sensor_name, '" and ', '"', laser_sensor_name, '" in "', str(list(depth_topics.keys())[1:]), '"'])),
        #     package='depthimage_to_laserscan',
        #     executable='depthimage_to_laserscan_node',
        #     remappings=[('depth', depth_topics[depth_sensor_name][0]),
        #                 ('depth_camera_info', depth_topics[depth_sensor_name][1])],
        #     parameters=[fake_laser_config_path]
        # ) 
    ])

   