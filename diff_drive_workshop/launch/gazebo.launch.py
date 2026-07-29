"""
gazebo.launch.py
─────────────────
Launches the complete assembled robot in Gazebo (Ignition Fortress — default
for ROS 2 Humble).

Uses the SOLVED assembly so the simulation works even before students
complete the placeholders.

USAGE (from the diff_drive_workshop directory):

    ros2 launch launch/gazebo.launch.py

After launch, drive the robot:

    ros2 topic pub /cmd_vel geometry_msgs/msg/Twist \
    "{linear: {x: 0.2}}" --once

    ros2 topic pub /cmd_vel geometry_msgs/msg/Twist \
    "{angular: {z: 0.5}}" --once
"""

import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command

from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():

    pkg_ros_gz_sim = get_package_share_directory("ros_gz_sim")

    pkg_dir = os.path.dirname(os.path.abspath(__file__))

    urdf_file = os.path.join(
        pkg_dir,
        "..",
        "urdf",
        "05_robot_assembly_SOLUTION.urdf.xml",
    )

    robot_description = ParameterValue(
        Command(["cat ", urdf_file]),
        value_type=str,
    )

    # ── robot_state_publisher ────────────────────────────────────────

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[
            {
                "robot_description": robot_description,
                "use_sim_time": True,
            }
        ],
    )

    # ── Gazebo (Ignition Fortress) ───────────────────────────────────

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                pkg_ros_gz_sim,
                "launch",
                "gz_sim.launch.py",
            )
        ),
        launch_arguments={
            "gz_args": "-r empty.sdf"
        }.items(),
    )

    # ── Spawn robot into Gazebo ──────────────────────────────────────

    spawn_robot = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=[
            "-name",
            "diff_drive_robot",
            "-topic",
            "/robot_description",
            "-x",
            "0.0",
            "-y",
            "0.0",
            "-z",
            "0.1",
        ],
        output="screen",
    )

    # ── Bridge ROS 2 ↔ Ignition topics ──────────────────────────────

    bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[
            "/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist",
            "/odom@nav_msgs/msg/Odometry@gz.msgs.Odometry",
            "/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock",
            "/world/empty/model/diff_drive_robot/joint_state"
            "@sensor_msgs/msg/JointState[gz.msgs.Model",
        ],
        remappings=[
            (
                "/world/empty/model/diff_drive_robot/joint_state",
                "/joint_states",
            )
        ],
        output="screen",
    )

    return LaunchDescription(
        [
            robot_state_publisher,
            gazebo,
            spawn_robot,
            bridge,
        ]
    )
