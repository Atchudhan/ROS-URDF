"""
workshop_rviz.launch.py
────────────────────────
Launches robot_state_publisher + joint_state_publisher_gui + RViz2
so students can visualise each URDF file without a full ROS 2 package.

USAGE (from the diff_drive_workshop directory):
  ros2 launch launch/workshop_rviz.launch.py
  ros2 launch launch/workshop_rviz.launch.py urdf:=urdf/01_chassis.urdf.xml
"""

import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():

    _launch_dir = os.path.dirname(os.path.abspath(__file__))

    # ── Launch arguments ─────────────────────────────────────────────
    urdf_arg = DeclareLaunchArgument(
        "urdf",
        default_value=os.path.join(
            _launch_dir, "..", "urdf", "04_robot_assembly.urdf.xml"
        ),
        description="Absolute or CWD-relative path to the URDF file",
    )

    rviz_config_arg = DeclareLaunchArgument(
        "rviz_config",
        default_value=os.path.join(_launch_dir, "..", "rviz", "robot_view.rviz"),
        description="Path to RViz2 config file",
    )

    # ── Robot description (read URDF file) ───────────────────────────
    robot_description = ParameterValue(
        Command(["cat ", LaunchConfiguration("urdf")]), value_type=str
    )

    # ── Nodes ────────────────────────────────────────────────────────
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[
            {
                "robot_description": robot_description,
                "use_sim_time": False,
            }
        ],
    )

    joint_state_publisher_gui = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        name="joint_state_publisher_gui",
        output="screen",
    )

    rviz2 = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", LaunchConfiguration("rviz_config")],
    )

    return LaunchDescription(
        [
            urdf_arg,
            rviz_config_arg,
            robot_state_publisher,
            joint_state_publisher_gui,
            rviz2,
        ]
    )
