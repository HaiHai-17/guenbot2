from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.substitutions import PathJoinSubstitution
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    sensors_launch_path = PathJoinSubstitution(
        [FindPackageShare('guenbot2_bringup'), 'launch', 'sensors.launch.py']
    )

    description_launch_path = PathJoinSubstitution(
        [FindPackageShare('guenbot2_description'), 'launch', 'description.launch.py']
    )

    return LaunchDescription([
        #run robot driver
        #https://github.com/linorobot/sphero_rvr
        Node(
            package='sphero_rvr',
            executable='sphero_node',
            name='sphero_node',
            output='screen'
        ),
        #https://github.com/christianrauch/raspicam2_node
        Node(
            package='raspicam2',
            executable='raspicam2_node',
            name='raspicam2',
            output='screen'
        ),
        #you can load your custom urdf launcher here
        #for demo's sake we'll use the default description launch file
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(description_launch_path)
        ),
        #hardware/sensor specific launch files
        #for demo's sake we'll use the default description launch file
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(sensors_launch_path),
        )
    ])