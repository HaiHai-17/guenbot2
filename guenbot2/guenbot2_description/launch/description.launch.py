import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command, PathJoinSubstitution, EnvironmentVariable
from launch.conditions import IfCondition
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    robot_base = "mecanum"

    urdf_path = PathJoinSubstitution(
        # [FindPackageShare("guenbot2_description"), "urdf/robots", f"{robot_base}.urdf.xacro"]
        # [FindPackageShare("guenbot2_description"), "urdf", "Assem1.urdf"]
        [FindPackageShare("guenbot2_description"), "urdf", "guenbot2.urdf"]
    )

    rviz_config_path = PathJoinSubstitution(
        [FindPackageShare('guenbot2_description'), 'rviz', 'description.rviz']
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            name='urdf', 
            default_value=urdf_path,
            description='URDF path'
        ),
        
        DeclareLaunchArgument(
            name='publish_joints', 
            default_value='true',
            description='Launch joint_states_publisher'
        ),

        DeclareLaunchArgument(
            name='rviz', 
            default_value='false',
            description='Run rviz'
        ),

        DeclareLaunchArgument(
            name='use_sim_time', 
            default_value='true',
            description='Use simulation time'
        ),

        # Node(
        #     package='v4l2_camera',
        #     executable='v4l2_camera_node',
        #     output='screen',
        #     parameters=[{
        #         'image_size': [1080,720],
        #         'camera_frame_id': 'camera_link_optical'}
        #     ]
        # ),

        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            condition=IfCondition(LaunchConfiguration("publish_joints")),
            parameters=[
                {'use_sim_time': LaunchConfiguration('use_sim_time')}
            ]
        ),

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[
                {
                    'use_sim_time': LaunchConfiguration('use_sim_time'),
                    'robot_description': ParameterValue(Command(['xacro ', LaunchConfiguration('urdf')]), value_type=str),
                }
            ]
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', rviz_config_path],
            condition=IfCondition(LaunchConfiguration("rviz")),
            parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}]
        )
    ])