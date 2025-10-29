import os
from ament_index_python.packages import get_package_share_directory
import launch
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import IncludeLaunchDescription, ExecuteProcess, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    # 获取包路径
    go2_description_path = get_package_share_directory('go2_description')
    
    # URDF 文件路径
    urdf_file = os.path.join(go2_description_path, 'urdf', 'go2_description.urdf')
    
    # RViz 配置文件路径
    rviz_config_file = os.path.join(go2_description_path, 'launch', 'check_joint_rviz2.rviz')
    
    # 读取 URDF 文件内容
    with open(urdf_file, 'r') as file:
        robot_description = file.read()
    
    # 使用仿真时间（与 Gazebo 同步）
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    
    # Joint State Publisher GUI - 用于手动控制关节
    # 静态 TF 变换发布器: base_link -> base_footprint
    tf_footprint_publisher = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='tf_footprint_publisher',
        arguments=['0', '0', '0', '0', '0', '0', 'base', 'base_footprint']
    )


    joint_state_publisher_gui = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        parameters=[
            {'robot_description': robot_description},
            {'use_sim_time': use_sim_time}
        ],
        output='screen'
    )

    # Robot State Publisher - 发布机器人的 TF 变换
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[
            {'robot_description': robot_description},
            {'publish_frequency': 1000.0},
            {'use_sim_time': use_sim_time}
        ],
        output='screen'
    )

    # RViz2 - 可视化工具
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_file],
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen'
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation time (set to true when using with Gazebo)'
        ),
        joint_state_publisher_gui,
        tf_footprint_publisher,
        robot_state_publisher,
        rviz
    ])
    
