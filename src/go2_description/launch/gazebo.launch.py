import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    # 获取包路径
    go2_description_path = get_package_share_directory('go2_description')
    ros_gz_sim_path = get_package_share_directory('ros_gz_sim')
    
    # URDF 文件路径
    urdf_file = os.path.join(go2_description_path, 'urdf', 'go2_description.urdf')

    # 读取 URDF 文件内容并替换 package:// 路径为绝对路径
    with open(urdf_file, 'r') as file:
        robot_desc = file.read()
    
    # 将 package://go2_description 替换为 file:// 绝对路径
    robot_desc = robot_desc.replace('package://go2_description', 'file://' + go2_description_path)

    # 包含 ros_gz_sim gz_sim.launch.py
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim_path, 'launch', 'gz_sim.launch.py')
        ),
    )

    # 静态 TF 变换发布器: base_link -> base_footprint
    tf_footprint_base = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='tf_footprint_base',
        arguments=['0', '0', '0', '0', '0', '0', 'base_link', 'base_footprint']
    )

    # 在 Gazebo 中生成模型 - 使用 --string 传递处理后的 URDF 内容
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        name='spawn_model',
        arguments=['--string', robot_desc,
                   '-name', 'go2_description',
                   '-allow_renaming', 'true',
                   '-z', '1.0'],
        output='screen'
    )

    # 发布校准消息
    fake_joint_calibration = ExecuteProcess(
        cmd=['ros2', 'topic', 'pub', '/calibrated', 'std_msgs/msg/Bool', 
             '{data: true}', '--once'],
        output='screen'
    )

    return LaunchDescription([
        gazebo,
        tf_footprint_base,
        spawn_entity,
        fake_joint_calibration,
    ])

